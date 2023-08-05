/*
  Based on Jean-Francois Romang work from
  https://github.com/jromang/Stockfish/blob/pyfish/src/pyfish.cpp
*/

#include <Python.h>

#include "misc.h"
#include "types.h"
#include "bitboard.h"
#include "evaluate.h"
#include "position.h"
#include "search.h"
#include "syzygy/tbprobe.h"
#include "thread.h"
#include "tt.h"
#include "uci.h"

static PyObject* PySFishError;

namespace PSQT {
  void init();
}

using namespace std;

namespace
{

static const char* PieceToChar[COLOR_NB] = { " PNBRHEQK", " pnbrheqk" };

const string move_to_san(Position& pos, Move m) {
  Bitboard others, b;
  string san;
  Color us = pos.side_to_move();
  Square from = from_sq(m);
  Square to = to_sq(m);
  Piece pc = pos.piece_on(from);
  PieceType pt = type_of(pc);

  if (type_of(m) == CASTLING)
      {
        san = to > from ? "O-O" : "O-O-O";

        if (is_gating(m))
        {
          san += string("/") + PieceToChar[WHITE][gating_type(m)];
          san += gating_on_to_sq(m) ? UCI::square(to) : UCI::square(from);
        }
      }
  else
  {
      if (pt != PAWN)
      {
          san = PieceToChar[WHITE][pt]; // Upper case

          // A disambiguation occurs if we have more then one piece of type 'pt'
          // that can reach 'to' with a legal move.
          others = b = (pos.attacks_from(pt, to) & pos.pieces(us, pt)) ^ from;

          while (b)
          {
              Square s = pop_lsb(&b);
              if (!pos.legal(make_move(s, to)))
                  others ^= s;
          }

          if (!others)
              { /* disambiguation is not needed */ }
          else if (!(others & file_bb(from)))
              san += UCI::square(from)[0];
          else if (!(others & rank_bb(from)))
              san += UCI::square(from)[1];
          else
              san += UCI::square(from)[0];
      }
      else if (pos.capture(m))
          san = UCI::square(from)[0];

      if (pos.capture(m))
          san += 'x';

      san += UCI::square(to);

      if (type_of(m) == PROMOTION)
          san += string("=") + PieceToChar[WHITE][promotion_type(m)];
      else if (is_gating(m))
          san += string("/") + PieceToChar[WHITE][gating_type(m)];
  }

  if (pos.gives_check(m))
  {
      StateInfo st;
      pos.do_move(m, st);
      san += MoveList<LEGAL>(pos).size() ? "+" : "#";
      pos.undo_move(m);
  }
  return san;
}

// FEN string of the initial position
const char* StartFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR[HEhe] w KQBCDFGkqbcdfg - 0 1";

bool hasInsufficientMaterial(Color c, Position *p) {
    if (p->count<PAWN>(c) > 0 || p->count<ROOK>(c) > 0 || p->count<QUEEN>(c) > 0 || p->count<HAWK>(c) > 0 || p->count<ELEPHANT>(c) > 0)
        return false;

    if (p->count<KNIGHT>(c) + p->count<BISHOP>(c) < 2)
        return true;

    if (p->count<BISHOP>(c) > 1 && p->count<KNIGHT>(c) == 0) {
        bool sameColor;
        sameColor = ((DarkSquares & (p->pieces(c, BISHOP))) == 0) || ((~DarkSquares & (p->pieces(c, BISHOP))) == 0);
        return sameColor;
    }
    return false;
}

bool buildPosition(Position *pos, const char *fen, PyObject *moveList, bool detectCheck) {
    bool givesCheck = false;
    StateListPtr states = StateListPtr(new std::deque<StateInfo>(1));

    if(strcmp(fen,"startpos")==0) fen=StartFEN;
    pos->set(fen, Options["UCI_Chess960"], &states->back(), Threads.main());

    // parse move list
    int numMoves = PyList_Size(moveList);
    for (int i=0; i<numMoves ; i++) {
        string moveStr( PyBytes_AS_STRING(PyUnicode_AsEncodedString( PyList_GetItem(moveList, i), "UTF-8", "strict")) );
        Move m;
        if ((m = UCI::to_move(*pos, moveStr)) != MOVE_NONE)
        {
            if (detectCheck && i==numMoves-1) givesCheck = pos->gives_check(m);
            // do the move
            states->emplace_back();
            pos->do_move(m, states->back());
        }
        else
        {
            PyErr_SetString(PyExc_ValueError, (string("Invalid move '")+moveStr+"'").c_str());
        }
    }
    return givesCheck;
}

}

extern "C" PyObject* pysfish_info(PyObject* self) {
    return Py_BuildValue("s", engine_info().c_str());
}

// INPUT option name, option value
extern "C" PyObject* pysfish_setOption(PyObject* self, PyObject *args) {
    const char *name;
    PyObject *valueObj;
    if (!PyArg_ParseTuple(args, "sO", &name, &valueObj)) return NULL;

    if (Options.count(name))
        Options[name] = string(PyBytes_AS_STRING(PyUnicode_AsEncodedString(PyObject_Str(valueObj), "UTF-8", "strict")));
    else
    {
        PyErr_SetString(PyExc_ValueError, (string("No such option ")+name+"'").c_str());
        return NULL;
    }
    Py_RETURN_NONE;
}

// INPUT fen, move
extern "C" PyObject* pysfish_getSAN(PyObject* self, PyObject *args) {
    PyObject* moveList = PyList_New(0);
    Position pos;
    const char *fen, *move;

    if (!PyArg_ParseTuple(args, "ss", &fen,  &move)) {
        return NULL;
    }
    buildPosition(&pos, fen, moveList, false);
    string moveStr = move;
    return Py_BuildValue("s", move_to_san(pos, UCI::to_move(pos, moveStr)).c_str());
}

// INPUT fen, list of moves
extern "C" PyObject* pysfish_legalMoves(PyObject* self, PyObject *args) {
    PyObject* legalMoves = PyList_New(0), *moveList;
    Position pos;
    const char *fen;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }

    buildPosition(&pos, fen, moveList, false);
    for (const auto& m : MoveList<LEGAL>(pos))
    {
        PyObject *moveStr;
        moveStr=Py_BuildValue("s", UCI::move(m, false).c_str());
        PyList_Append(legalMoves, moveStr);
        Py_XDECREF(moveStr);
    }

    return legalMoves;
}

// Input FEN, list of moves
extern "C" PyObject* pysfish_getFEN(PyObject* self, PyObject *args) {
    PyObject *moveList;
    Position pos;
    const char *fen;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }
    buildPosition(&pos, fen, moveList, false);
    return Py_BuildValue("s", pos.fen().c_str());
}

// Input FEN, list of moves
extern "C" PyObject* pysfish_givesCheck(PyObject* self, PyObject *args) {
    PyObject *moveList;
    Position pos;
    const char *fen;
    bool givesCheck;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }
    if (PyList_Size(moveList) < 1) {
        PyErr_SetString(PyExc_ValueError, (string("Move list can't be empty.")).c_str());
        return NULL;
    }
    givesCheck = buildPosition(&pos, fen, moveList, true);
    return Py_BuildValue("O", givesCheck ? Py_True : Py_False);
}

// INPUT variant, fen, move list
extern "C" PyObject* pyffish_isOptionalGameEnd(PyObject* self, PyObject *args) {
    PyObject *moveList;
    Position pos;
    const char *fen;
    bool gameEnd;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }

    buildPosition(&pos, fen, moveList, false);
    gameEnd = pos.is_draw(0);
    return Py_BuildValue("(Oi)", gameEnd ? Py_True : Py_False, 0);
}

// INPUT variant, fen, move list
extern "C" PyObject* pyffish_hasInsufficientMaterial(PyObject* self, PyObject *args) {
    PyObject *moveList;
    Position pos;
    const char *fen;
    bool wInsufficient, bInsufficient;

    if (!PyArg_ParseTuple(args, "sO!", &fen,  &PyList_Type, &moveList)) {
        return NULL;
    }

    buildPosition(&pos, fen, moveList, false);
    wInsufficient = hasInsufficientMaterial(WHITE, &pos);
    bInsufficient = hasInsufficientMaterial(BLACK, &pos);
    return Py_BuildValue("(OO)", wInsufficient ? Py_True : Py_False, bInsufficient ? Py_True : Py_False);
}

static PyMethodDef PySFishMethods[] = {
    {"info", (PyCFunction)pysfish_info, METH_NOARGS, "Get Stockfish version info."},
    {"set_option", (PyCFunction)pysfish_setOption, METH_VARARGS, "Set UCI option."},
    {"get_san", (PyCFunction)pysfish_getSAN, METH_VARARGS, "Get SAN move from given FEN and UCI move."},
    {"legal_moves", (PyCFunction)pysfish_legalMoves, METH_VARARGS, "Get legal moves from given FEN and movelist."},
    {"get_fen", (PyCFunction)pysfish_getFEN, METH_VARARGS, "Get resulting FEN from given FEN and movelist."},
    {"gives_check", (PyCFunction)pysfish_givesCheck, METH_VARARGS, "Get check status from given FEN and movelist."},
    {"is_optional_game_end", (PyCFunction)pyffish_isOptionalGameEnd, METH_VARARGS, "Get result from given FEN it rules enable game end by player."},
    {"has_insufficient_material", (PyCFunction)pyffish_hasInsufficientMaterial, METH_VARARGS, "Set UCI option."},
    {NULL, NULL, 0, NULL},  // sentinel
};

static PyModuleDef pysfishmodule = {
    PyModuleDef_HEAD_INIT,
    "pysfish",
    "Seirawan-Stockfish extension module.",
    -1,
    PySFishMethods,
};

PyMODINIT_FUNC PyInit_pysfish() {
    PyObject* module;

    module = PyModule_Create(&pysfishmodule);
    if (module == NULL) {
        return NULL;
    }
    PySFishError = PyErr_NewException("pysfish.error", NULL, NULL);
    Py_INCREF(PySFishError);
    PyModule_AddObject(module, "error", PySFishError);

    // initialize stockfish
    UCI::init(Options);
    PSQT::init();
    Bitboards::init();
    Position::init();
    Bitbases::init();
    Search::init();
    Pawns::init();
    Tablebases::init(Options["SyzygyPath"]);
    TT.resize(Options["Hash"]);
    Threads.set(Options["Threads"]);
    Search::clear(); // After threads are up

    return module;
};

from typing import List, Tuple

from thriftpy2.thrift import TType


def get_python_type(ttype: int, is_required: bool, meta: List) -> str:
    type_map = {
        TType.BOOL: _get_bool,
        TType.DOUBLE: _get_double,
        TType.BYTE: _get_byte,
        TType.I16: _get_i16,
        TType.I32: _get_i32,
        TType.I64: _get_i64,
        TType.STRING: _get_str,
        TType.STRUCT: _get_struct,
        TType.MAP: _get_map,
        TType.SET: _get_set,
        TType.LIST: _get_list,
    }
    pytype = type_map[ttype](meta)
    if not is_required:
        pytype = f"Optional[{pytype}]"
    return pytype


def _get_bool(meta: List) -> str:
    del meta
    return "bool"


def _get_double(meta: List) -> str:
    del meta
    return "float"


def _get_byte(meta: List) -> str:
    del meta
    return "int"


def _get_i16(meta: List) -> str:
    del meta
    return "int"


def _get_i32(meta: List) -> str:
    del meta
    return "int"


def _get_i64(meta: List) -> str:
    del meta
    return "int"


def _get_str(meta: List) -> str:
    del meta
    return "str"


def _get_struct(meta: List) -> str:
    return f"{meta[0].__module__}.{meta[0].__name__}"


def _get_list(meta: List) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"List[{get_python_type(subttype, True, submeta)}]"


def _get_map(meta: List) -> str:
    key, value = meta[0]
    key_ttype, key_meta = _unpack_meta([key])
    value_ttype, value_meta = _unpack_meta([value])
    key_pytype = get_python_type(key_ttype, True, key_meta)
    value_pytype = get_python_type(value_ttype, True, value_meta)
    return f"Dict[{key_pytype}, {value_pytype}]"


def _get_set(meta: List) -> str:
    subttype, submeta = _unpack_meta(meta)
    return f"Set[{get_python_type(subttype, True, submeta)}]"


def _unpack_meta(meta: List) -> Tuple[int, List]:
    try:
        subttype, submeta = meta[0]
    except TypeError:
        subttype, submeta = meta[0], None
    return subttype, [submeta]

# Conexão do postgres com o python
from contextlib import contextmanager

from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

from . import config

_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = SimpleConnectionPool(1, 5, dsn=config.DATABASE_URL)
    return _pool


@contextmanager
def cursor():
    """Entrega um cursor (linhas como dict). Faz commit no sucesso, rollback no erro
    e sempre devolve a conexão ao pool."""
    pool = _get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)

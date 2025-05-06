#!/usr/bin/env python3

import http.client
import logging
import random

HOST = "httpstat.us"
TIMEOUT = 10  

CODES = {
    "1xx": [100, 101, 102, 103],                           
    "2xx": [200, 201, 202, 203, 205, 206, 207, 208, 226],
    "3xx": [300, 301, 302, 303, 305, 306, 307, 308],  
    "4xx": [400, 404, 418, 429, 451],
    "5xx": [500, 502, 503, 504, 520, 523, 527],
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def fetch(code: int) -> tuple[int, str, str]:
    """
    Возвращает (status_code, reason_phrase, body).
    Используем прямое соединение через http.client.
    """
    conn = http.client.HTTPConnection(HOST, 80, timeout=TIMEOUT)
    conn.request("GET", f"/{code}")
    resp = conn.getresponse()

    status, reason = resp.status, resp.reason
    body = resp.read().decode().strip() or f"{status} {reason}".strip()
    conn.close()
    return status, reason, body


def handle(code: int) -> None:
    status, reason, body = fetch(code)

    if status < 400:                       # 1xx-3xx
        logging.info("OK    %s – %s", status, body)
    else:                                  # 4xx-5xx
        raise RuntimeError(f"ERROR {status} – {body}")


def main() -> None:
    
    codes = [random.choice(v) for v in CODES.values()]

    for idx, code in enumerate(codes, 1):
        try:
            handle(code)
        except Exception as exc:
            logging.error("Запрос #%d: %s", idx, exc)


if __name__ == "__main__":
    main()
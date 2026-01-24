import sys

print(sys.executable)  # Покажет путь к Python, который запущен
try:
    import aiohttp

    print("Успех! Библиотека найдена.")
except ImportError:
    print("Библиотека всё еще не видна для этого интерпретатора.")

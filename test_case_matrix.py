import aiohttp
import asyncio
from typing import List

async def get_matrix(url: str) -> List[int]:
    """
    Асинхронно загружает матрицу с сервера и возвращает её обход по спирали против часовой стрелки.
    
    :param url: URL для загрузки матрицы
    :return: Список чисел, полученных при обходе матрицы по спирали
    :raises: ValueError, aiohttp.ClientError
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"Ошибка сервера: {response.status}")
                
                text = await response.text()
                matrix = parse_matrix(text)
                return spiral_traversal(matrix)
                
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        raise ValueError(f"Ошибка сети: {str(e)}")

def parse_matrix(text: str) -> List[List[int]]:
    """Парсит текст в матрицу чисел."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    matrix = []
    
    for line in lines:
        if '|' not in line:
            continue
            
        # Извлекаем числа между | символами
        parts = line.split('|')[1:-1]
        row = [int(num.strip()) for num in parts if num.strip()]
        matrix.append(row)
    
    # Проверяем, что матрица квадратная
    if not all(len(row) == len(matrix) for row in matrix):
        raise ValueError("Матрица не квадратная")
    
    return matrix

def spiral_traversal(matrix: List[List[int]]) -> List[int]:
    """Обходит матрицу по спирали против часовой стрелки."""
    if not matrix:
        return []
    
    n = len(matrix)
    result = []
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    
    while top <= bottom and left <= right:
        # Проходим вниз по левому краю
        for i in range(top, bottom + 1):
            result.append(matrix[i][left])
        left += 1
        
        # Проходим вправо по нижней строке
        for i in range(left, right + 1):
            result.append(matrix[bottom][i])
        bottom -= 1
        
        if left <= right:
            # Проходим вверх по правому краю
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
            right -= 1
        
        if top <= bottom:
            # Проходим влево по верхней строке
            for i in range(right, left - 1, -1):
                result.append(matrix[top][i])
            top += 1
    
    return result

# Пример использования (для тестирования)
if __name__ == "__main__":
    async def main():
        url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
        try:
            result = await get_matrix(url)
            print("Результат обхода:", result)
        except ValueError as e:
            print("Ошибка:", e)
    
    asyncio.run(main())


SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

def test_get_matrix():
    assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL
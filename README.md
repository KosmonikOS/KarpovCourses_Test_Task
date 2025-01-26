## Создание RAG-сервиса для навигации по курсам

### Step 0: Введение в задачу

Вы работаете разработчиком в образовательной платформе. На последней встрече руководитель отдела поддержки поднял важный вопрос:

"Наши студенты часто задают похожие вопросы о выборе курсов. Они хотят понять, какой курс им больше подходит, чем курсы отличаются друг от друга, и какие навыки они получат. Сейчас менеджеры тратят много времени на однотипные ответы. Как мы можем автоматизировать этот процесс?"

Для решения этой проблемы было предложено создать умный чат-бот на основе технологии RAG (Retrieval-Augmented Generation). Бот будет анализировать описания курсов и отвечать на вопросы студентов, помогая им сделать правильный выбор.

### Step 1: Обработчик Web страниц

В этом шаге мы создадим компонент для загрузки и обработки веб-страниц с описаниями курсов. Основная задача - получить текстовое содержимое страниц и разбить его на оптимальные фрагменты для дальнейшей обработки.

#### Теория: Рекурсивное разбиение текста

Рекурсивное разбиение текста (Recursive Character Text Splitting) - это метод разделения длинных текстов на меньшие фрагменты с сохранением семантической целостности. Основные принципы:

1. **Иерархическое разбиение:**
   - Текст сначала разбивается по крупным разделителям (абзацы, заголовки)
   - Затем по более мелким (предложения, фразы)
   - И наконец, по отдельным словам, если необходимо

2. **Перекрытие фрагментов:**
   - Каждый фрагмент включает часть предыдущего/следующего фрагмента
   - Это помогает сохранить контекст и связность
   - Размер перекрытия обычно 10-20% от размера фрагмента

3. **Контроль размера:**
   - Фрагменты должны быть достаточно большими для сохранения контекста
   - Но не слишком большими для эффективной обработки
   - Рекомендуемый размер: 500-1000 символов

#### Задание

Вам нужно реализовать класс `WebPageProcessor` для загрузки и обработки веб-страниц. Используйте следующий шаблон:

```python
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class WebPageProcessor:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        """Initialize document processor
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        # TODO: Инициализируйте параметры разбиения
        pass

    def process_urls(self, urls: List[str]) -> List[str]:
        """Load URLs and split into chunks
        Args:
            urls: List of URLs to process
        Returns:
            List of text chunks
        """
        # TODO: 
        # 1. Загрузите документы используя WebBaseLoader
        # 2. Создайте сплиттер с заданными параметрами
        # 3. Разбейте документы на фрагменты
        # 4. Верните список текстовых фрагментов
        pass
```

#### Распределение баллов
- 100% - Код верно обрабатывает web страницы и возвращает фрагменты

#### Полезные ссылки
1. [LangChain RecursiveCharacterTextSplitter](https://python.langchain.com/docs/how_to/recursive_text_splitter/) - Документация по рекурсивному разбиению текста, включая примеры и рекомендации по настройке
2. [LangChain WebBaseLoader](https://python.langchain.com/docs/integrations/document_loaders/web_base/) - Документация по загрузчику веб-страниц, описание параметров и примеры использования

### Step 2: Векторные представления текста

В этом шаге мы создадим компонент для преобразования текстовых фрагментов в векторные представления (эмбеддинги). Это ключевой компонент для реализации семантического поиска.

#### Теория: Word Embeddings

Векторные представления (эмбеддинги) - это способ преобразования текста в числовые векторы, где семантически похожие тексты оказываются близко друг к другу в векторном пространстве. Основные преимущества:

1. **Семантический поиск:**
   - Возможность находить похожие тексты даже при использовании разных слов
   - Понимание контекста и смысла, а не только точное совпадение

2. **Эффективность:**
   - Быстрый поиск похожих документов через векторные операции
   - Компактное представление текста фиксированной размерности

3. **Многоязычность:**
   - Возможность сравнивать тексты на разных языках
   - Единое векторное пространство для всех языков

4. **Нормализация векторов:**
   - Приведение векторов к единичной длине (L2-нормализация)
   - После нормализации скалярное произведение равно косинусному сходству
   - Нормализация должна выполняться на этапе создания эмбеддингов
   - Векторное хранилище ожидает уже нормализованные векторы

#### Задание

Вам нужно реализовать класс `Embedder` для создания векторных представлений текста. Используйте следующий шаблон:

```python
import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
import torch


class Embedder:
    def __init__(
        self, model_name: str = "intfloat/multilingual-e5-small", device: str = None
    ):
        """Initialize the embedder with a SentenceTransformer model
        Args:
            model_name: Name of the model to use (default: intfloat/multilingual-e5-small)
            device: Device to use for inference (default: auto-detect)
        """
        # TODO: 
        # 1. Определите устройство для вычислений (cpu, cuda, mps)
        # 2. Загрузите модель SentenceTransformer
        pass

    def get_embeddings(self, texts: list[str]) -> NDArray[np.float32]:
        """Get embeddings for a list of texts
        Args:
            texts: List of texts to embed
        Returns:
            NDArray of embeddings as float32
        """
        # TODO:
        # 1. Используйте модель для получения эмбеддингов
        # 2. Нормализуйте эмбеддинги
        # 3. Преобразуйте результат в numpy array типа float32
        # 4. Обработайте возможные ошибки
        pass

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        # TODO: Верните размерность эмбеддингов модели
        pass
```

#### Распределение баллов
- 100% - Код верно создает векторные представления текстов

#### Полезные ссылки
1. [Sentence-BERT](https://sbert.net) - Официальная документация библиотеки SentenceTransformers, включая примеры использования и описание архитектуры
2. [multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small) - Модель, которую мы используем для создания эмбеддингов, поддерживает более 100 языков
3. [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084) - Научная статья, описывающая архитектуру и принципы работы Sentence-BERT

### Step 3: Векторное хранилище

В этом шаге мы создадим компонент для эффективного хранения и поиска векторных представлений текста.

#### Теория: Косинусное сходство и векторные базы данных

1. **Косинусное сходство:**
   - Это метрика, измеряющая угол между векторами в многомерном пространстве
   - Значения от -1 (противоположные) до 1 (идентичные)
   - Не зависит от длины векторов, только от их направления
   - Идеально подходит для сравнения текстовых эмбеддингов

2. **Нормализация векторов:**
   - Приведение векторов к единичной длине (L2-нормализация)
   - После нормализации скалярное произведение равно косинусному сходству
   - Нормализация должна выполняться на этапе создания эмбеддингов
   - Векторное хранилище ожидает уже нормализованные векторы

3. **Зачем нужны векторные базы данных:**
   - **Эффективность:** Обычные базы данных не оптимизированы для поиска по векторам. Поиск ближайших соседей в многомерном пространстве - сложная задача.
   - **Масштабируемость:** Векторные БД используют специальные индексы для быстрого поиска похожих векторов.
   - **Производительность:** Оптимизированы для параллельных вычислений на CPU/GPU.

4. **FAISS (Facebook AI Similarity Search):**
   - Библиотека для эффективного поиска похожих векторов
   - Поддерживает различные типы индексов и метрик сходства
   - Оптимизирована для работы с большими наборами данных
   - Может использовать GPU для ускорения

#### Задание

Реализуйте класс `VectorStore` для хранения и поиска векторных представлений. Используйте следующий шаблон:

```python
import numpy as np
import faiss
import json
from numpy.typing import NDArray


class VectorStore:
    def __init__(self, dimension: int):
        """Initialize FAISS index with inner product similarity (cosine similarity for normalized vectors)
        Args:
            dimension: Dimension of the vectors (depends on the embedder model)
        """
        # TODO: 
        # 1. Создайте FAISS индекс с заданной размерностью (используйте IndexFlatIP)
        # 2. Инициализируйте список для хранения текстов
        pass

    def add_texts(self, texts: list[str], embeddings: NDArray[np.float32]) -> None:
        """Add texts and their embeddings to the index.
        Vectors must be L2-normalized before passing to this method.
        Args:
            texts: List of texts to add
            embeddings: Array of L2-normalized embeddings as float32
        """
        # TODO:
        # 1. Проверьте корректность входных данных
        # 2. Добавьте эмбеддинги в индекс
        # 3. Сохраните соответствующие тексты
        pass

    def similarity_search(
        self, query_embedding: NDArray[np.float32], k: int = 5
    ) -> list[dict[str, float]]:
        """Search for most similar vectors using cosine similarity.
        Query vector must be L2-normalized before passing to this method.
        Args:
            query_embedding: L2-normalized query embedding as float32 array
            k: Number of results to return (will be capped by number of stored texts)
        Returns:
            List of dictionaries containing chunk and score for all retrieved chunks
        """
        # TODO:
        # 1. Подготовьте query_embedding для поиска (reshape в 2D если нужно)
        # 2. Проверьте корректность k
        # 3. Найдите ближайшие векторы используя inner product
        # 4. Верните результаты в виде списка словарей
        pass

    def save(self, path: str) -> None:
        """Save the vector store to files
        Args:
            path: Base path for saving files (without extension)
        """
        # TODO:
        # 1. Сохраните FAISS индекс
        # 2. Сохраните тексты в JSON файл
        pass

    def load(self, path: str) -> None:
        """Load the vector store from files
        Args:
            path: Base path for loading files (without extension)
        """
        # TODO:
        # 1. Загрузите FAISS индекс
        # 2. Загрузите тексты из JSON файла
        pass
```

#### Распределение баллов
- 40% - Корректная реализация добавления текстов
- 30% - Корректная реализация поиска векторов
- 30% - Корректное сохранение и загрузка данных

#### Полезные ссылки
1. [FAISS](https://github.com/facebookresearch/faiss) - Библиотека для эффективного поиска похожих векторов, документация и примеры использования
2. [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity) - Подробное описание косинусного сходства и его применения в векторном поиске

### Step 4: Советник по курсам

В этом шаге мы создадим компонент, который будет использовать языковую модель для генерации персонализированных ответов на основе найденной информации о курсах.

#### Теория: Использование LLM для синтеза ответов

Языковые модели (LLM - Large Language Models) могут быть использованы для создания осмысленных ответов на основе контекста. Основные принципы:

1. **Промпт-инжиниринг:**
   - Структурированная подача контекста и вопроса
   - Четкие инструкции для модели
   - Ограничения на формат ответа

2. **Контекстное обучение:**
   - Модель использует предоставленный контекст
   - Не полагается только на предобученные знания
   - Может комбинировать информацию из разных источников

3. **Преимущества RAG подхода:**
   - Актуальность информации в ответах
   - Возможность цитирования источников
   - Контроль над содержанием ответов

#### Задание

Реализуйте класс `CourseAdvisor` для генерации ответов на вопросы о курсах. Используйте следующий шаблон:

```python
import os
from openai import OpenAI
from config import QA_PROMPT
from vector_store import VectorStore
from embedder import Embedder


class CourseAdvisor:
    def __init__(self, vectorstore: VectorStore, embedder: Embedder):
        """Initialize course advisor with vector store and embedder
        Args:
            vectorstore: VectorStore instance for course content search
            embedder: Embedder instance for question embedding
        """
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
        self.model = os.getenv("OPENAI_MODEL")
        # TODO:
        # 1. Инициализируйте клиент OpenAI с переменными окружения
        # 2. Сохраните ссылки на vectorstore и embedder

    def retrieve_context(self, question: str) -> list[str]:
        """Retrieve relevant course content for the question
        Args:
            question: Question about courses
        Returns:
            List of relevant course content chunks
        """
        # TODO:
        # 1. Получите эмбеддинг для вопроса
        # 2. Найдите похожие фрагменты в vectorstore
        # 3. Верните список найденных фрагментов
        pass

    def generate_completion(self, question: str, context: str,**kwargs) -> str:
        """Generate course advice using OpenAI API
        Args:
            question: Question about courses
            context: Relevant course content to use for answering
        Returns:
            Generated course advice
        """
        # TODO:
        # 1. Отформатируйте промпт с вопросом и контекстом
        # 2. Создайте запрос к OpenAI API
        # 3. Обработайте возможные ошибки
        # 4. Верните сгенерированный ответ
        pass

    def process_query(self, question: str, **kwargs) -> str:
        """Process a course-related question and generate advice
        Args:
            question: Question about courses
        Returns:
            Generated course advice based on relevant content
        """
        # TODO:
        # 1. Получите релевантный контекст
        # 2. Объедините фрагменты контекста
        # 3. Сгенерируйте и верните ответ
        pass
```

Используйте следующий промпт для генерации ответов:
```
Ты - профессиональный консультант по образовательным программам Karpov.Courses. Твоя задача - помочь студентам выбрать наиболее подходящий курс, основываясь на предоставленной информации о курсах и потребностях студента.

Контекст о курсах:
{context}

Вопрос студента:
{question}

Пожалуйста, следуй этим правилам при составлении ответа:
1. Если вопрос не связан с курсами или выбором образовательной программы, ответь: "Извините, я могу помочь только с вопросами о курсах Karpov.Courses и подбором подходящей образовательной программы."
2. Для вопросов о курсах:
   - Внимательно проанализируй информацию о курсах из контекста
   - Дай четкую и конкретную рекомендацию, основываясь на вопросе студента
   - Объясни, почему именно этот курс(ы) подходит студенту
   - Укажи основные навыки, которые студент получит после прохождения курса
   - Если информации недостаточно для рекомендации, укажи только те курсы, которые могут подойти, исходя из имеющейся информации
3. Ответ должен быть на русском языке и содержать только финальную рекомендацию без дополнительных вопросов
```

#### Распределение баллов
- 40% - Корректная работа с контекстом и векторным поиском
- 30% - Правильная работа с OpenAI API
- 30% - Качество генерируемых ответов

#### Полезные ссылки
1. [OpenAI Python Library](https://github.com/openai/openai-python) - Официальная библиотека Python для работы с OpenAI API, включая примеры использования и обработку ошибок

### Step 5: Веб-интерфейс

В этом шаге мы интегрируем наше решение в веб-приложение с помощью Streamlit.

#### Теория: Streamlit

Streamlit - это фреймворк для быстрого создания веб-приложений на Python. Основные преимущества:

1. **Простота:**
   - Минимум кода для создания интерфейса
   - Автоматическое обновление при изменении данных
   - Встроенные компоненты для визуализации

2. **Python-центричность:**
   - Не требует знания HTML/CSS/JavaScript
   - Интеграция с популярными библиотеками (pandas, numpy)
   - Поддержка асинхронных операций

3. **Продакшн-готовность:**
   - Встроенный веб-сервер
   - Поддержка кэширования
   - Простой деплой

#### Задание

1. Склонируйте репозиторий с базовой реализацией:
```bash
git clone https://github.com/KosmonikOS/KarpovCourses_Test_Task
cd KarpovCourses_Test_Task
```

2. Замените следующие файлы своей реализацией:
   - `app/course_advisor.py`
   - `app/vector_store.py`
   - `app/web_page_processor.py`
   - `app/embedder.py`

3. Зарегестрируйтесь на [Groq AI](https://groq.com) и получите API ключ.

4. Создайте файл `.env` со следующими переменными:
```
OPENAI_API_KEY=groq_api_key
OPENAI_BASE_URL=https://api.groq.com/openai/v1/
OPENAI_MODEL=llama-3.3-70b-versatile
VECTOR_STORE_PATH=vectorstore
```

5. Установите зависимости и запустите сервис:
```bash
pip install -r requirements.txt
streamlit run app/app.py
```

6. Протестируйте работу сервиса:


### Step 6: Поздравляем!

🎉 Поздравляем с успешным выполнением задания! Вы создали полноценный RAG-сервис, который помогает студентам выбирать подходящие курсы.

#### Чему вы научились

В процессе выполнения задания вы освоили ключевые компоненты современных AI-систем:

1. **Обработка веб-контента:**
   - Загрузка данных с веб-страниц
   - Очистка HTML-разметки
   - Разбиение текста на семантические фрагменты

2. **Векторные представления:**
   - Работа с эмбеддингами текста
   - Использование предобученных моделей
   - Оптимизация вычислений на GPU/CPU

3. **Векторные базы данных:**
   - Принципы векторного поиска
   - Работа с FAISS индексами
   - Оптимизация поиска ближайших соседей

4. **Языковые модели:**
   - Промпт-инжиниринг
   - Работа с LLM API
   - Контекстная генерация ответов

5. **Веб-разработка:**
   - Создание интерактивных интерфейсов
   - Работа со Streamlit
   - Управление состоянием приложения

#### Практические навыки

- Написание чистого, типизированного Python-кода
- Работа с современными AI-библиотеками
- Обработка ошибок и граничных случаев
- Тестирование AI-компонентов
- Развертывание AI-сервисов

Эти знания и навыки являются основой для разработки современных AI-приложений и высоко ценятся на рынке труда.

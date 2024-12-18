from setuptools import setup, find_packages

setup(
    name="group_cases",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pytest',
        'openai>=1.40',
        'tiktoken',
        'msal',
        'rich',
        'requests',
        'chevron',
        'llama-index',
        'llama-index-embeddings-huggingface',
        'llama-index-readers-web',
        'pypandoc',
        'docx',
        'markdown',
        'jupyter',
        'streamlit'
    ],
)

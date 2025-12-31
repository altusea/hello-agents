import dotenv


def read_deepseek_api_key():
    """Read DeepSeek API key from .env file in home directory."""
    return read_dot_env_val("DEEPSEEK_API_KEY")


def read_dot_env_val(key: str) -> str:
    """Read a value from .env file in home directory."""
    file_path = dotenv.find_dotenv(usecwd=True)
    val = dotenv.dotenv_values(file_path).get(key)
    if val is None:
        raise ValueError(f"{key} not found in .env file.")
    return val


if __name__ == "__main__":
    print(read_deepseek_api_key())

"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast
import math
import sys
import io

from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

from react_agent.configuration import Configuration


async def search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_context()
    wrapped = TavilySearch(max_results=configuration.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


async def sin_tool(x: float) -> dict[str, float]:
    """计算输入值的正弦值。

    该函数接收一个浮点数x，返回其正弦值。适用于需要三角函数计算的场景。

    Args:
        x (float): 输入的角度值（以弧度为单位）。

    Returns:
        dict[str, float]: 包含输入值和正弦值的字典。
    """
    return {"input": x, "sin": math.sin(x)}


async def cos_tool(x: float) -> dict[str, float]:
    """计算输入值的余弦值。

    该函数接收一个浮点数x，返回其余弦值。适用于需要三角函数计算的场景。

    Args:
        x (float): 输入的角度值（以弧度为单位）。

    Returns:
        dict[str, float]: 包含输入值和余弦值的字典。
    """
    return {"input": x, "cos": math.cos(x)}


def exec_python_code(code: str) -> dict[str, str]:
    """在本地Python环境中运行输入的Python代码，并返回运行结果。

    该函数接收一段Python代码字符串，在本地环境中执行，并返回标准输出和异常信息。

    Args:
        code (str): 需要执行的Python代码。

    Returns:
        dict[str, str]: 包含标准输出和异常信息的字典。
    """
    stdout = io.StringIO()
    stderr = io.StringIO()
    result = {"stdout": "", "stderr": ""}
    try:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = stdout
        sys.stderr = stderr
        exec(code, {})
    except Exception as e:
        result["stderr"] = str(e)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        result["stdout"] = stdout.getvalue()
        if not result["stderr"]:
            result["stderr"] = stderr.getvalue()
    return result


TOOLS: List[Callable[..., Any]] = [search, sin_tool, cos_tool, exec_python_code]

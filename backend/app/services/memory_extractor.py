# ============================================================
# 多智能体记忆中枢 - 记忆提取服务
# ============================================================
# 功能：从对话中自动提取关键信息
# 作者：小码
# 日期：2026-03-06
# ============================================================

import json
import logging
from typing import Optional
import httpx

from ..models.conversation import MemoryExtractionResult, ExtractedMemory
from ..config import settings

logger = logging.getLogger(__name__)


class MemoryExtractor:
    """记忆提取服务：从对话中提取关键信息"""
    
    def __init__(self):
        """初始化提取器，使用统一配置"""
        # LLM API 配置（使用统一配置）
        self.llm_api_url = f"{settings.LLM_BASE_URL}/chat/completions"
        self.llm_api_key = settings.DASHSCOPE_LLM_API_KEY
        self.llm_model = settings.LLM_MODEL
        
        # 是否启用 LLM 提取（默认启用）
        self.enabled = True
        
        # 提取 prompt 模板
        self.extraction_prompt = """你是一个信息提取助手，负责从对话中提取关键信息。

请从以下对话中提取关键信息，以 JSON 格式返回：

对话内容：
{conversation}

请提取以下类型的信息：
1. facts（事实）：用户的个人信息、偏好、习惯等客观信息
2. relationships（关系）：用户与AI或其他人的关系描述
3. events（事件）：重要的时间、地点、约定等事件信息
4. emotions（情感）：用户表达的情感状态

返回格式（仅返回 JSON，不要有其他内容）：
{{
    "facts": ["事实1", "事实2"],
    "relationships": ["关系1"],
    "events": ["事件1"],
    "emotions": ["情感1"]
}}

如果没有某类信息，该字段返回空数组。

示例：
对话：
用户：我是憨货，喜欢用吐槽风格聊天
AI：好的，我记住了，以后用吐槽风格和你聊

返回：
{{
    "facts": ["用户名叫憨货", "用户喜欢吐槽风格聊天"],
    "relationships": [],
    "events": [],
    "emotions": []
}}

现在请提取上述对话的信息："""

    async def extract_memories(
        self, 
        conversation_text: str
    ) -> MemoryExtractionResult:
        """
        从对话中提取关键信息
        
        Args:
            conversation_text: 对话文本
        
        Returns:
            提取结果
        """
        if not self.enabled:
            logger.info("记忆提取功能已禁用")
            return MemoryExtractionResult()
        
        try:
            # 调用 LLM API
            result = await self._call_llm(conversation_text)
            
            # 解析 JSON 结果
            extraction_result = self._parse_extraction_result(result)
            
            logger.info(
                f"提取完成: facts={len(extraction_result.facts)}, "
                f"relationships={len(extraction_result.relationships)}, "
                f"events={len(extraction_result.events)}, "
                f"emotions={len(extraction_result.emotions)}"
            )
            
            return extraction_result
            
        except Exception as e:
            logger.error(f"记忆提取失败: {e}", exc_info=True)
            # 提取失败时返回空结果，而不是抛出异常
            return MemoryExtractionResult()
    
    async def _call_llm(self, conversation_text: str) -> str:
        """
        调用 LLM API
        
        Args:
            conversation_text: 对话文本
        
        Returns:
            LLM 返回的文本
        
        Raises:
            Exception: API 调用失败
        """
        prompt = self.extraction_prompt.format(conversation=conversation_text)
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.llm_api_key:
            headers["Authorization"] = f"Bearer {self.llm_api_key}"
        
        payload = {
            "model": self.llm_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # 低温度，更确定性的输出
            "max_tokens": 1000
        }
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                self.llm_api_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(
                    f"LLM API 调用失败: status={response.status_code}, "
                    f"body={response.text}"
                )
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    def _parse_extraction_result(self, result_text: str) -> MemoryExtractionResult:
        """
        解析提取结果
        
        Args:
            result_text: LLM 返回的文本
        
        Returns:
            解析后的提取结果
        """
        try:
            # 尝试直接解析 JSON
            data = json.loads(result_text)
            
            return MemoryExtractionResult(
                facts=data.get("facts", []),
                relationships=data.get("relationships", []),
                events=data.get("events", []),
                emotions=data.get("emotions", [])
            )
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 解析失败，尝试提取: {e}")
            
            # 尝试提取 JSON 块
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    return MemoryExtractionResult(
                        facts=data.get("facts", []),
                        relationships=data.get("relationships", []),
                        events=data.get("events", []),
                        emotions=data.get("emotions", [])
                    )
                except json.JSONDecodeError:
                    pass
            
            # 解析失败，返回空结果
            logger.error(f"无法解析提取结果: {result_text[:200]}")
            return MemoryExtractionResult()
    
    def update_config(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        enabled: Optional[bool] = None
    ):
        """
        更新配置
        
        Args:
            api_url: API URL
            api_key: API Key
            model: 模型名称
            enabled: 是否启用
        """
        if api_url is not None:
            self.llm_api_url = api_url
        if api_key is not None:
            self.llm_api_key = api_key
        if model is not None:
            self.llm_model = model
        if enabled is not None:
            self.enabled = enabled
        
        logger.info(
            f"配置已更新: url={self.llm_api_url}, "
            f"model={self.llm_model}, enabled={self.enabled}"
        )


# 全局服务实例
memory_extractor = MemoryExtractor()
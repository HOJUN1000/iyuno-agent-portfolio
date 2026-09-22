import torch


DEFAULT_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


class QwenGenerator:
    """
    Qwen-based answer generator.

    An already-loaded tokenizer/model can be injected to avoid
    loading duplicate model copies in memory.
    """

    def __init__(
        self,
        tokenizer,
        model,
        max_new_tokens=250,
    ):
        if tokenizer is None:
            raise ValueError("tokenizer cannot be None.")

        if model is None:
            raise ValueError("model cannot be None.")

        self.tokenizer = tokenizer
        self.model = model
        self.max_new_tokens = max_new_tokens


    def generate(
        self,
        question,
        context,
    ):
        """Generate an evidence-grounded answer."""

        if not isinstance(question, str) or not question.strip():
            raise ValueError(
                "Question must be a non-empty string."
            )

        if not isinstance(context, str) or not context.strip():
            raise ValueError(
                "Context must be a non-empty string."
            )

        system_prompt = (
            "You are a security knowledge assistant. "
            "Answer ONLY using the provided context. "
            "Do not invent facts or use unsupported outside knowledge. "
            "If the context is insufficient, explicitly say that "
            "there is insufficient evidence in the collected documentation. "
            "Keep the answer concise and factual."
        )

        user_prompt = (
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            [text],
            return_tensors="pt",
        )

        # 모델이 올라가 있는 장치로 입력 이동
        try:
            device = next(
                self.model.parameters()
            ).device

            inputs = {
                key: value.to(device)
                for key, value in inputs.items()
            }

        except StopIteration:
            pass

        with torch.inference_mode():

            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
            )

        # 입력 prompt 부분 제거
        output_ids = generated_ids[
            :,
            inputs["input_ids"].shape[1]:
        ]

        answer = self.tokenizer.batch_decode(
            output_ids,
            skip_special_tokens=True,
        )[0].strip()

        return answer

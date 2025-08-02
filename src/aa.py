from strands import Agent
from strands.models.openai import OpenAIModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from tools import show_files, read_json, send_email_report, analyze_and_generate_pdf
import gradio as gr
from config import api_key

# إعداد النموذج
model = OpenAIModel(
    client_args={"api_key": api_key},
    model_id="gpt-4o",
    params={"max_tokens": 1000, "temperature": 0.7},
)

# إعداد مدير المحادثة
conversation_manager = SlidingWindowConversationManager(window_size=20)

# تعريف prompt
prompt = """
🛡️ You are an AI Cybersecurity Analyst...
(نفس محتوى البرومبت)
"""

# إنشاء الـ Agent
agent = Agent(
    model=model,
    tools=[show_files, read_json, send_email_report, analyze_and_generate_pdf],
    system_prompt=prompt,
    conversation_manager=conversation_manager
)

# Gradio Interface
def run_agent_command(user_input):
    try:
        return agent(user_input)
    except Exception as e:
        return f"❌ Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("## 🛡️ SentinelGuard AI – SOC Agent Interface")
    with gr.Row():
        input_box = gr.Textbox(label="Enter your command", placeholder="e.g., show files or analyze ransomware_logs.json")
        output_box = gr.Textbox(label="Agent Output", lines=15)
    run_button = gr.Button("Run Agent")
    run_button.click(fn=run_agent_command, inputs=[input_box], outputs=[output_box])

demo.launch()

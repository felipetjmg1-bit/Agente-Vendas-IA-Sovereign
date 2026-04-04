import gradio as gr
import pandas as pd
from lead_automation import automate_lead_qualification

def process_leads(csv_file, api_key_input, qualification_threshold_input):
    if csv_file is None:
        return "Por favor, carregue um arquivo CSV.", pd.DataFrame(), pd.DataFrame()

    # Salvar o arquivo carregado temporariamente
    csv_path = "uploaded_leads.csv"
    with open(csv_path, "wb") as f:
        f.write(csv_file.read())

    output_df = automate_lead_qualification(csv_path, api_key_input, qualification_threshold_input)

    if not output_df.empty:
        qualified_output = output_df[output_df["status"] == "Qualified"]
        unqualified_output = output_df[output_df["status"] == "Unqualified"]
        return "Processamento concluído!", qualified_output, unqualified_output
    else:
        return "Nenhum lead processado ou erro no arquivo.", pd.DataFrame(), pd.DataFrame()


iface = gr.Interface(
    fn=process_leads,
    inputs=[
        gr.File(label="Carregar CSV de Leads"),
        gr.Textbox(label="Sua Chave de API de IA (Simulada)", type="password"),
        gr.Slider(minimum=0.1, maximum=0.9, step=0.05, value=0.7, label="Limiar de Qualificação"),
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Dataframe(label="Leads Qualificados"),
        gr.Dataframe(label="Leads Não Qualificados"),
    ],
    title="Agente de Vendas com IA Soberana - Qualificação de Leads",
    description="Carregue seu arquivo CSV de leads para qualificá-los automaticamente usando IA. Este é um exemplo de prova de conceito."
)

iface.launch()

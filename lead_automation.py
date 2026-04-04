import pandas as pd
import requests
import json

def automate_lead_qualification(lead_data_path, api_key, qualification_threshold=0.7):
    """
    Automatiza a qualificação de leads usando uma API de IA para análise de texto.

    Args:
        lead_data_path (str): Caminho para o arquivo CSV com os dados dos leads.
        api_key (str): Chave da API para o serviço de análise de texto (ex: OpenAI, Gemini).
        qualification_threshold (float): Limiar de qualificação (0 a 1).

    Returns:
        pd.DataFrame: DataFrame com leads qualificados e não qualificados.
    """
    try:
        leads_df = pd.read_csv(lead_data_path)
    except FileNotFoundError:
        print(f"Erro: Arquivo {lead_data_path} não encontrado.")
        return pd.DataFrame()

    qualified_leads = []
    unqualified_leads = []

    for index, lead in leads_df.iterrows():
        company_description = lead.get('company_description', '')
        contact_notes = lead.get('contact_notes', '')
        text_to_analyze = f"Descrição da Empresa: {company_description}. Notas de Contato: {contact_notes}"

        # Simulação de chamada de API de IA para qualificação
        # Em um cenário real, você integraria com uma API como Gemini ou OpenAI
        # Exemplo simplificado:
        try:
            # Supondo uma API que retorna um score de qualificação
            # Esta é uma simulação. A implementação real dependeria da API escolhida.
            response = requests.post(
                "https://api.example.com/ai-qualifier", # Substituir pela URL da API real
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={
                    "prompt": f"Analise o seguinte texto para qualificação de lead B2B para soluções de IA e automação. Retorne um score de 0 a 1, onde 1 é altamente qualificado: {text_to_analyze}",
                    "max_tokens": 50
                }
            )
            response.raise_for_status()
            ai_response = response.json()
            # Simulação de extração do score
            score_text = ai_response.get('choices', [{}])[0].get('text', 'Score: 0.5')
            score = float(score_text.split('Score: ')[-1])
        except Exception as e:
            print(f"Erro ao chamar API de IA para o lead {lead.get('id', index)}: {e}")
            score = 0.5 # Valor padrão em caso de erro

        if score >= qualification_threshold:
            qualified_leads.append({**lead.to_dict(), 'qualification_score': score, 'status': 'Qualified'})
        else:
            unqualified_leads.append({**lead.to_dict(), 'qualification_score': score, 'status': 'Unqualified'})

    return pd.DataFrame(qualified_leads + unqualified_leads)

if __name__ == "__main__":
    # Exemplo de uso
    # Crie um arquivo leads.csv para testar
    # id,company_name,company_description,contact_name,contact_email,contact_notes
    # 1,TechCorp,"Empresa de software, busca otimização de processos",João Silva,joao@techcorp.com,"Interesse em automação de atendimento"
    # 2,RetailPro,"Rede de varejo, precisa de análise de estoque",Maria Souza,maria@retailpro.com,"Mencionou desafios com gestão manual"
    # 3,SmallBiz,"Pequeno comércio, sem foco em tecnologia",Carlos Lima,carlos@smallbiz.com,"Apenas curiosidade, sem necessidade imediata"

    # Substitua 'SUA_API_KEY_AQUI' pela sua chave real da API de IA
    api_key = "SUA_API_KEY_AQUI"
    output_df = automate_lead_qualification('leads.csv', api_key)

    if not output_df.empty:
        qualified_output = output_df[output_df['status'] == 'Qualified']
        unqualified_output = output_df[output_df['status'] == 'Unqualified']

        print("\n--- Leads Qualificados ---")
        print(qualified_output.to_markdown(index=False))

        print("\n--- Leads Não Qualificados ---")
        print(unqualified_output.to_markdown(index=False))

        output_df.to_csv('qualified_leads_report.csv', index=False)
        print("\nRelatório de leads salvo em 'qualified_leads_report.csv'")

    else:
        print("Nenhum lead processado.")

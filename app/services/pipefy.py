import logging

logger = logging.getLogger(__name__)

PIPEFY_PIPE_ID = "your_pipe_id"


def build_create_card_mutation(nome, email, tipo_solicitacao, valor_patrimonio):
    mutation = """
    mutation CreateCard($input: CreateCardInput!) {
      createCard(input: $input) {
        card {
          id
          title
          current_phase { name }
          fields { name value }
        }
      }
    }
    """
    variables = {
        "input": {
            "pipe_id": PIPEFY_PIPE_ID,
            "title": f"Solicitação - {nome}",
            "fields_attributes": [
                {"field_id": "cliente_nome", "field_value": nome},
                {"field_id": "cliente_email", "field_value": email},
                {"field_id": "tipo_solicitacao", "field_value": tipo_solicitacao},
                {"field_id": "valor_patrimonio", "field_value": str(valor_patrimonio)}
            ]
        }
    }
    payload = {"query": mutation, "variables": variables}
    logger.info("[PIPEFY SIMULADO] createCard: %s", payload)
    return payload


def build_update_card_field_mutation(card_id, novo_status, prioridade):
    mutation = """
    mutation UpdateCardField($input: UpdateCardFieldInput!) {
      updateCardField(input: $input) {
        success
        clientMutationId
      }
    }
    """
    status_payload = {"query": mutation, "variables": {"input": {"card_id": card_id, "field_id": "status_cliente", "new_value": novo_status}}}
    prioridade_payload = {"query": mutation, "variables": {"input": {"card_id": card_id, "field_id": "prioridade_cliente", "new_value": prioridade}}}
    logger.info("[PIPEFY SIMULADO] updateCardField status: %s", status_payload)
    logger.info("[PIPEFY SIMULADO] updateCardField prioridade: %s", prioridade_payload)
    return {"status_payload": status_payload, "prioridade_payload": prioridade_payload}

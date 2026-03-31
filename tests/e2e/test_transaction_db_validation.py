from core.db_client import DBClient

def test_transaction_db_validation(api_client):

    # Step 1: Create transaction via API
    api_client.post("/transactions", {"amount": 300})

    # Step 2: Validate in DB
    db = DBClient()

    result = db.execute_query(
        "SELECT amount FROM transactions ORDER BY id DESC LIMIT 1"
    )

    db.close()

    assert result[0][0] == 300
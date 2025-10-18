import asyncio
from routes.data.schemas import AlertCreate
from core.logic import db_data_to_df

async def main():
    payload = AlertCreate(contract="NQ1!", trade_type="buy", quantity=1, price=100.0, name="algo1")
    df = await db_data_to_df([payload])
    print("COLUMNS:", list(df.columns))
    print(df.to_dict(orient='records'))

if __name__ == '__main__':
    asyncio.run(main())


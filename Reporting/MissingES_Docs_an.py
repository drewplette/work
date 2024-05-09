import pandas as pd
import aiohttp
import asyncio
import pyodbc

#Access the SQL Server database and read the data into a pandas DataFrame
sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=[server_name];DATABASE=[database_name];UID=[user_id];PWD=[password]')
query = "SELECT DISTINCT[document_id] AS 'Document ID' FROM [dbo].[document] WHERE document id != 0"  # Update with your table name

df = pd.read_sql(query, sql_conn)
sql_conn.close()


# List to store document IDs not found in the index
    
async def check_documents(docs, session):
    async def check_document(doc_id):
        url = url_template.format(doc_id)
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Document {doc_id} not found.")
                not_found_docs.append(doc_id)

    tasks = [check_document(doc_id) for doc_id in docs]
    await asyncio.gather(*tasks)

async def main():
    batch_size = 100  # You can adjust this based on your requirements
    for i in range(0, len(df), batch_size):
        batch_ids = df["Document ID"].iloc[i:i+batch_size].tolist()
        async with aiohttp.ClientSession() as session:
            await check_documents(batch_ids, session)

# Run the asynchronous main function

base_url = "[ES_URL]"
index_name = "[ES_DOC_PUB_INDEX_NAME]"
not_found_docs = []
url_template = f"{base_url}/{index_name}/_doc/{{}}"
asyncio.run(main())

# Print the list of document IDs not found
if not_found_docs:
    print("\nDocument IDs not found in the index:")
    for doc_id in not_found_docs:
        print(doc_id)
    # Create a DataFrame from the not_found_docs list
    not_found_df = pd.DataFrame({"Document ID": not_found_docs})
    # Save the DataFrame to a new Excel file
    not_found_excel_file = index_name + "_results.xlsx"  # Update with desired file path
    not_found_df.to_excel(not_found_excel_file, index=False)
    print(f"\nNot found document IDs saved to '{not_found_excel_file}'.")
else:
    print("\nAll document IDs are found in the index.")

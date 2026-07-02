import psycopg2

attempts = [
    dict(host='aws-0-ap-southeast-2.pooler.supabase.com', port=6543, dbname='postgres', user='postgres', password='BuildMyGame@2026'),
    dict(host='aws-0-ap-southeast-2.pooler.supabase.com', port=5432, dbname='postgres', user='postgres.ragnazpjjwcizacxwdvc', password='BuildMyGame@2026'),
    dict(host='aws-0-ap-southeast-2.pooler.supabase.com', port=5432, dbname='postgres', user='postgres', password='BuildMyGame@2026'),
]
for i, kw in enumerate(attempts):
    try:
        conn = psycopg2.connect(**kw, connect_timeout=5)
        cur = conn.cursor()
        cur.execute('SELECT 1')
        user = kw["user"]
        port = kw["port"]
        print(f"Attempt {i+1}: OK! user={user} port={port}")
        cur.close()
        conn.close()
        break
    except Exception as e:
        user = kw["user"]
        port = kw["port"]
        err = str(e)[:100]
        print(f"Attempt {i+1}: FAIL (user={user} port={port}) -> {err}")

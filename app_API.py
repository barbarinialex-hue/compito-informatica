from flask import Flask, jsonify
from flask_cors import CORS
from utils.db import get_db_connection, serialize_row

app = Flask(__name__)
CORS(app)

# ----------------- API -----------------
@app.route('/api/ordine/<int:id_ordine>')
def get_ordine(id_ordine):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "DB offline"}), 200

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.*, m.DataMissione, m.Ora, m.LatPrelievo, m.LongPrelievo,
                   m.LatConsegna, m.LongConsegna, m.Valutazione, m.Commento,
                   m.IdDrone, m.IdPilota, m.Stato,
                   d.Modello, p.Nome as NomePilota, p.Cognome as CognomePilota
            FROM Ordine o
            JOIN Missioni m ON o.ID_Missione = m.ID
            JOIN Drone d ON m.IdDrone = d.ID
            JOIN Pilota p ON m.IdPilota = p.ID
            WHERE o.ID = %s
        """, (id_ordine,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(serialize_row(row)), 200
    except Exception as e:
        print("❌ ERRORE /api/ordine:", e)
        return jsonify({"error": str(e)}), 200

@app.route('/api/missione/<int:id_missione>')
def get_missione(id_missione):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "DB offline"}), 200

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, d.Modello, p.Nome, p.Cognome
            FROM Missioni m
            JOIN Drone d ON m.IdDrone = d.ID
            JOIN Pilota p ON m.IdPilota = p.ID
            WHERE m.ID = %s
        """, (id_missione,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(serialize_row(row)), 200
    except Exception as e:
        print("❌ ERRORE /api/missione:", e)
        return jsonify({"error": str(e)}), 200

@app.route('/api/traccia/<int:id_missione>')
def get_traccia(id_missione):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify([]), 200

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.Latitudine, t.Longitudine, t.TIMESTAMP
            FROM Traccia t
            WHERE t.ID_Missione = %s
            ORDER BY t.TIMESTAMP
        """, (id_missione,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([serialize_row(r) for r in rows]), 200
    except Exception as e:
        print("❌ ERRORE /api/traccia:", e)
        return jsonify([]), 200

@app.route('/api/missioni')
def get_missioni():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify([]), 200

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.ID, m.Stato, m.DataMissione, m.Ora, m.Valutazione,
                   d.Modello, CONCAT(p.Nome, ' ', p.Cognome) as Pilota,
                   COUNT(t.TIMESTAMP) as NumTracce
            FROM Missioni m
            JOIN Drone d ON m.IdDrone = d.ID
            JOIN Pilota p ON m.IdPilota = p.ID
            LEFT JOIN Traccia t ON t.ID_Missione = m.ID
            GROUP BY m.ID
            ORDER BY m.DataMissione DESC
            LIMIT 20
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([serialize_row(r) for r in rows]), 200
    except Exception as e:
        print("❌ ERRORE /api/missioni:", e)
        return jsonify([]), 200

if __name__ == '__main__':
    print("🚀 API SERVER Flask pronto sulla porta 5001")
    app.run(debug=True, port=5001, host='0.0.0.0')

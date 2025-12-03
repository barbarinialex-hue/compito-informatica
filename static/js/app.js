let map, polyline, markers = [];

const API_BASE = 'http://127.0.0.1:5001/api';

async function updateOrdine() {
    const idOrdine = document.getElementById('ordine-id').value;
    const ordineResp = await fetch(`${API_BASE}/ordine/${idOrdine}`);
    const ordine = await ordineResp.json();
    console.log(ordine);

    // Richiama missione e traccia come prima usando API_BASE
}

map = L.map('map').setView([45.4642, 9.1900], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

function clearMap() {
    if (polyline) map.removeLayer(polyline);
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

async function updateOrdine() {
    try {
        const idOrdine = document.getElementById('ordine-id').value;
        const ordineResp = await fetch(`/api/ordine/${idOrdine}`);
        const ordine = await ordineResp.json();

        if (!ordine.ID) return alert('Ordine non trovato!');

        const missioneResp = await fetch(`/api/missione/${ordine.ID_Missione}`);
        const missione = await missioneResp.json();

        document.getElementById('stato').textContent = missione.Stato;
        document.getElementById('stato').className = `stato-${missione.Stato?.replace(/ /g, '_')}`;
        document.getElementById('drone').textContent = ordine.Modello || 'N/D';
        document.getElementById('pilota').textContent = `${ordine.NomePilota} ${ordine.CognomePilota}` || 'N/D';
        document.getElementById('valutazione').textContent = missione.Valutazione || 'N/D';

        const tracciaResp = await fetch(`/api/traccia/${ordine.ID_Missione}`);
        const tracce = await tracciaResp.json();
        clearMap();

        if (tracce?.length > 0) {
            polyline = L.polyline(tracce.map(t => [t.Latitudine, t.Longitudine]), {
                color: 'blue',
                weight: 4
            }).addTo(map);

            map.fitBounds(polyline.getBounds());

            L.marker([missione.LatPrelievo, missione.LongPrelievo], {
                icon: L.divIcon({ html: '📦' })
            }).addTo(map).bindPopup('Prelievo');

            L.marker([missione.LatConsegna, missione.LongConsegna], {
                icon: L.divIcon({ html: '✅' })
            }).addTo(map).bindPopup('Consegna');

            const ultima = tracce[tracce.length - 1];
            L.marker([ultima.Latitudine, ultima.Longitudine]).addTo(map)
                .bindPopup(`Ultimo: ${new Date(ultima.TIMESTAMP).toLocaleString()}`);
        }
    } catch (e) {
        console.error('Errore API:', e);
        document.getElementById('stato').textContent = 'Errore connessione';
    }
}

setInterval(updateOrdine, 3000);
document.getElementById('refresh-btn').onclick = updateOrdine;
document.getElementById('ordine-id').onchange = updateOrdine;
document.getElementById('all-missioni').onclick = () => window.open('/api/missioni', '_blank');

updateOrdine();

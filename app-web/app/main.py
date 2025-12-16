from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator
from app.controllers.hotel_controller import router as hotel_router
from app.controllers.chambre_controller import router as chambre_router
from app.controllers.client_controller import router as client_router
from app.controllers.reservation_controller import router as reservation_router

app = FastAPI(title="TP Hôtel API", version="1.0.0")
Instrumentator().instrument(app).expose(app, include_in_schema=False)
app.include_router(hotel_router)
app.include_router(chambre_router)
app.include_router(client_router)
app.include_router(reservation_router)

@app.get("/", response_class=HTMLResponse)
def racine():
    # Page d'accueil simple avec des boutons de navigation
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8" />
        <title>TP Hôtel – Accueil API</title>
        <style>
            body {
                margin: 0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                color: #e5e7eb;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .container {
                max-width: 960px;
                width: 100%;
                padding: 2.5rem 2rem;
                background: rgba(15, 23, 42, 0.9);
                border-radius: 1rem;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.3);
            }
            h1 {
                font-size: 2rem;
                margin-bottom: 0.25rem;
                color: #f9fafb;
            }
            .subtitle {
                margin-bottom: 1.5rem;
                color: #9ca3af;
                font-size: 0.95rem;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 1.5rem;
            }
            .card {
                background: rgba(15, 23, 42, 0.9);
                border-radius: 0.75rem;
                padding: 1.25rem 1.5rem;
                border: 1px solid rgba(148, 163, 184, 0.25);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .card h2 {
                font-size: 1rem;
                margin: 0 0 0.25rem 0;
                color: #e5e7eb;
            }
            .card p {
                margin: 0 0 0.75rem 0;
                font-size: 0.85rem;
                color: #9ca3af;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.55rem 0.9rem;
                border-radius: 999px;
                border: none;
                cursor: pointer;
                text-decoration: none;
                font-size: 0.85rem;
                font-weight: 500;
                color: #0f172a;
                background: linear-gradient(135deg, #38bdf8, #22c55e);
                box-shadow: 0 10px 25px -8px rgba(34, 197, 94, 0.6);
                transition: transform 0.08s ease, box-shadow 0.08s ease, filter 0.08s ease;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
                box-shadow: 0 16px 30px -12px rgba(56, 189, 248, 0.7);
            }
            .btn:active {
                transform: translateY(0);
                box-shadow: 0 4px 14px -6px rgba(15, 23, 42, 0.8);
            }
            .tagline {
                font-size: 0.8rem;
                color: #6b7280;
                margin-top: 1rem;
            }
            .small {
                font-size: 0.78rem;
                color: #6b7280;
                margin-top: 1.5rem;
            }
            a {
                color: inherit;
            }
        </style>
    </head>
    <body>
        <main class="container">
            <header>
                <h1>TP – API REST de Gestion de Chambres d'Hôtel</h1>
                <p class="subtitle">
                    API pédagogique construite en architecture <strong>MVC</strong> pour gérer les hôtels, chambres,
                    clients et réservations d'une chaîne hôtelière.
                </p>
            </header>
            <section class="grid">
                <article class="card">
                    <div>
                        <h2>Documentation Swagger</h2>
                        <p>Consulter la description complète des endpoints REST (Hôtels, Chambres, Clients, Réservations).</p>
                    </div>
                    <a class="btn" href="/docs">Ouvrir les docs Swagger</a>
                </article>
                <article class="card">
                    <div>
                        <h2>Hôtels</h2>
                        <p>Tester les opérations de création et de consultation des hôtels du SI.</p>
                    </div>
                    <a class="btn" href="/hotels" target="_blank">GET /hotels</a>
                </article>
                <article class="card">
                    <div>
                        <h2>Chambres & disponibilité</h2>
                        <p>Gérer les chambres d'un hôtel et vérifier leur disponibilité selon le cahier des charges.</p>
                    </div>
                    <a class="btn" href="/hotels/1/chambres" target="_blank">GET /hotels/1/chambres</a>
                </article>
                <article class="card">
                    <div>
                        <h2>Clients & Réservations</h2>
                        <p>Explorer les endpoints de gestion des clients et des réservations (création / annulation).</p>
                    </div>
                    <a class="btn" href="/reservations" target="_blank">GET /reservations</a>
                </article>
            </section>
            <p class="small">
                Ce portail est un point d'entrée pour votre TP : utilisez Swagger pour créer hôtels, chambres,
                clients et réservations, puis revenez ici pour naviguer rapidement entre les ressources clés.
            </p>
        </main>
    </body>
    </html>
    """

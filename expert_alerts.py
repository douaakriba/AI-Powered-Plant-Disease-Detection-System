"""
PhytoSentinel — Système Expert pour Alertes Phytosanitaires
============================================================
Système expert basé sur des règles (IF-THEN) pour chaque culture.
Surveille les conditions météo et prédit les risques de maladies.
Génère des alertes avec recommandations pour les agriculteurs.
"""

from datetime import datetime
from typing import List, Dict, Optional

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE CONNAISSANCES — RÈGLES EXPERTES PAR CULTURE
# Structure : IF conditions météo THEN risque de maladie + recommandations
# ─────────────────────────────────────────────────────────────────────────────

EXPERT_KNOWLEDGE_BASE = {

    # ══════════════════════════════════════════════════════
    # 🍅 TOMATE
    # ══════════════════════════════════════════════════════
    "tomato": {
        "name_fr": "Tomate",
        "icon": "🍅",
        "rules": [
            {
                "id": "tomato_late_blight",
                "disease": "Mildiou de la Tomate (Late Blight)",
                "severity": "critical",
                "conditions": {
                    "temp_min": 15, "temp_max": 25,
                    "humidity_min": 75,
                    "rain_possible": True,
                },
                "check": lambda w: w["humidity"] >= 75 and 15 <= w["temp"] <= 25,
                "message": "Conditions très favorables au mildiou : température fraîche + humidité élevée. Risque d'infection en 24-48h.",
                "recommendations": [
                    "Appliquer de la bouillie bordelaise préventive dès maintenant",
                    "Retirer les feuilles basses touchant le sol",
                    "Éviter l'arrosage par aspersion le soir",
                    "Inspecter les plants quotidiennement",
                    "Assurer une bonne aération entre les rangs",
                ],
                "priority": 3,
            },
            {
                "id": "tomato_early_blight",
                "disease": "Alternariose (Early Blight)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 24, "temp_max": 35,
                    "humidity_min": 60,
                },
                "check": lambda w: w["humidity"] >= 60 and w["temp"] >= 24,
                "message": "Chaleur + humidité : risque modéré d'alternariose sur les feuilles âgées.",
                "recommendations": [
                    "Retirer les feuilles présentant des taches brunes concentriques",
                    "Traiter avec un fongicide à base de mancozèbe",
                    "Pailler le sol pour limiter les éclaboussures",
                    "Éviter les blessures mécaniques sur les plants",
                ],
                "priority": 2,
            },
            {
                "id": "tomato_bacterial_spot",
                "disease": "Bactériose (Bacterial Spot)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 25, "humidity_min": 70,
                    "wind_min": 20,
                },
                "check": lambda w: w["temp"] >= 25 and w["humidity"] >= 70 and w["wind"] >= 20,
                "message": "Vent fort + chaleur + humidité : le vent favorise la dispersion des bactéries.",
                "recommendations": [
                    "Éviter tout travail dans les cultures par temps humide et venteux",
                    "Appliquer un bactéricide à base de cuivre",
                    "Installer des brise-vent si possible",
                    "Désinfecter les outils après chaque utilisation",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🌽 MAÏS (CORN)
    # ══════════════════════════════════════════════════════
    "corn": {
        "name_fr": "Maïs",
        "icon": "🌽",
        "rules": [
            {
                "id": "corn_rust",
                "disease": "Rouille Commune du Maïs (Common Rust)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 16, "temp_max": 23,
                    "humidity_min": 70,
                },
                "check": lambda w: w["humidity"] >= 70 and 16 <= w["temp"] <= 23,
                "message": "Conditions favorables à la rouille du maïs : temps frais et humide.",
                "recommendations": [
                    "Surveiller l'apparition de pustules orangées sur les feuilles",
                    "Appliquer un fongicide triazole si infection détectée",
                    "Préférer des variétés hybrides résistantes pour la prochaine saison",
                    "Assurer un espacement suffisant entre les plants",
                ],
                "priority": 2,
            },
            {
                "id": "corn_leaf_blight",
                "disease": "Helminthosporiose (Northern Leaf Blight)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 18, "temp_max": 27,
                    "humidity_min": 75,
                },
                "check": lambda w: w["humidity"] >= 75 and 18 <= w["temp"] <= 27,
                "message": "Conditions humides prolongées : risque de brûlure foliaire du Nord.",
                "recommendations": [
                    "Inspecter les feuilles pour des lésions grisâtres elliptiques",
                    "Appliquer un fongicide systémique préventif",
                    "Assurer une bonne rotation des cultures (éviter maïs après maïs)",
                    "Retirer et brûler les résidus de culture infectés",
                ],
                "priority": 2,
            },
            {
                "id": "corn_gray_spot",
                "disease": "Cercosporiose (Gray Leaf Spot)",
                "severity": "low",
                "conditions": {
                    "temp_min": 25, "humidity_min": 80,
                },
                "check": lambda w: w["humidity"] >= 80 and w["temp"] >= 25,
                "message": "Humidité très élevée + chaleur : conditions favorables à la cercosporiose.",
                "recommendations": [
                    "Vérifier les feuilles inférieures pour des taches rectangulaires grises",
                    "Améliorer la circulation d'air entre les rangs",
                    "Appliquer un fongicide si l'incidence dépasse 5% des feuilles",
                ],
                "priority": 1,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🍎 POMME (APPLE)
    # ══════════════════════════════════════════════════════
    "apple": {
        "name_fr": "Pommier",
        "icon": "🍎",
        "rules": [
            {
                "id": "apple_scab",
                "disease": "Tavelure du Pommier (Apple Scab)",
                "severity": "critical",
                "conditions": {
                    "temp_min": 10, "temp_max": 24,
                    "humidity_min": 70,
                },
                "check": lambda w: w["humidity"] >= 70 and 10 <= w["temp"] <= 24,
                "message": "Printemps humide : risque élevé de tavelure. C'est la maladie la plus importante du pommier.",
                "recommendations": [
                    "Traitement fongicide OBLIGATOIRE avant les pluies (protecteur)",
                    "Appliquer du dithianon ou du myclobutanil",
                    "Ramasser et détruire les feuilles tombées (source d'infection)",
                    "Tailler pour améliorer l'aération du feuillage",
                    "Surveiller les prévisions de pluie avec l'outil météo",
                ],
                "priority": 3,
            },
            {
                "id": "apple_cedar_rust",
                "disease": "Rouille Grillagée (Cedar Apple Rust)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 15, "temp_max": 24,
                    "humidity_min": 65,
                    "wind_min": 10,
                },
                "check": lambda w: w["humidity"] >= 65 and 15 <= w["temp"] <= 24 and w["wind"] >= 10,
                "message": "Vent + humidité printanière : les spores de rouille peuvent se propager sur plusieurs km.",
                "recommendations": [
                    "Appliquer un fongicide triazole au débourrement",
                    "Éliminer les galls sur les genévriers proches si possible",
                    "Répéter le traitement toutes les 2 semaines en période humide",
                ],
                "priority": 2,
            },
            {
                "id": "apple_black_rot",
                "disease": "Pourriture Noire (Black Rot)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 20, "humidity_min": 60,
                },
                "check": lambda w: w["temp"] >= 20 and w["humidity"] >= 60,
                "message": "Chaleur et humidité : risque de pourriture noire sur les fruits et branches.",
                "recommendations": [
                    "Inspecter les fruits et branches pour des lésions brunâtres",
                    "Retirer immédiatement les momies (fruits momifiés) de l'arbre",
                    "Appliquer un fongicide captan ou thirame",
                    "Assurer une taille sanitaire pour éliminer le bois mort",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🥔 POMME DE TERRE (POTATO)
    # ══════════════════════════════════════════════════════
    "potato": {
        "name_fr": "Pomme de Terre",
        "icon": "🥔",
        "rules": [
            {
                "id": "potato_late_blight",
                "disease": "Mildiou de la Pomme de Terre (Late Blight)",
                "severity": "critical",
                "conditions": {
                    "temp_min": 10, "temp_max": 22,
                    "humidity_min": 75,
                },
                "check": lambda w: w["humidity"] >= 75 and 10 <= w["temp"] <= 22,
                "message": "ALERTE CRITIQUE : conditions parfaites pour le mildiou (Phytophthora infestans). Peut détruire 100% de la récolte en 1 semaine.",
                "recommendations": [
                    "⚡ URGENT : Appliquer du métalaxyl + mancozèbe IMMÉDIATEMENT",
                    "Traitement préventif toutes les 7 jours en période à risque",
                    "Éviter tout arrosage aérien - utiliser l'irrigation au goutte-à-goutte",
                    "Butter les rangs pour protéger les tubercules",
                    "Surveiller le bout des feuilles pour des taches brunes huileuses",
                    "Contacter immédiatement la DSA si infection confirmée",
                ],
                "priority": 3,
            },
            {
                "id": "potato_early_blight",
                "disease": "Alternariose (Early Blight)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 24, "humidity_min": 50,
                },
                "check": lambda w: w["temp"] >= 24 and w["humidity"] >= 50,
                "message": "Temps chaud : risque d'alternariose, surtout sur plants stressés ou âgés.",
                "recommendations": [
                    "Inspecter les vieilles feuilles pour des taches concentriques",
                    "Appliquer du chlorothalonil ou de l'iprodione",
                    "Assurer une fertilisation azotée équilibrée",
                    "Irrigation régulière pour éviter le stress hydrique",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🍇 VIGNE (GRAPE)
    # ══════════════════════════════════════════════════════
    "grape": {
        "name_fr": "Vigne",
        "icon": "🍇",
        "rules": [
            {
                "id": "grape_downy_mildew",
                "disease": "Mildiou de la Vigne (Plasmopara viticola)",
                "severity": "critical",
                "conditions": {
                    "temp_min": 13,
                    "humidity_min": 70,
                },
                "check": lambda w: w["humidity"] >= 70 and w["temp"] >= 13,
                "message": "Règle des '3 x 10' atteinte : risque élevé de mildiou. Les pousses sont vulnérables à partir de 10 cm.",
                "recommendations": [
                    "Traitement obligatoire à la bouillie bordelaise ou au fosetyl-Al",
                    "Intervenir avant la pluie (traitement préventif)",
                    "Ébourgeonnage pour améliorer l'aération",
                    "Surveiller le dessous des feuilles pour des taches huileuses",
                    "Répéter le traitement après chaque pluie importante (>10mm)",
                ],
                "priority": 3,
            },
            {
                "id": "grape_powdery_mildew",
                "disease": "Oïdium de la Vigne (Erysiphe necator)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 20, "temp_max": 32,
                    "humidity_min": 40, "humidity_max": 70,
                },
                "check": lambda w: w["temp"] >= 20 and 40 <= w["humidity"] <= 70,
                "message": "Temps chaud et sec : conditions idéales pour l'oïdium, même sans pluie.",
                "recommendations": [
                    "Traitement au soufre mouillable ou à la spiroxamine",
                    "Intervenir tôt le matin ou le soir (éviter la chaleur avec le soufre)",
                    "Tailler les sarments pour aérer la végétation",
                    "Répéter le traitement tous les 10-15 jours",
                ],
                "priority": 2,
            },
            {
                "id": "grape_black_rot",
                "disease": "Black Rot de la Vigne (Guignardia bidwellii)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 15, "humidity_min": 65,
                },
                "check": lambda w: w["humidity"] >= 65 and w["temp"] >= 15,
                "message": "Conditions humides : risque de black rot, surtout en période de floraison/fructification.",
                "recommendations": [
                    "Inspecter les grappes pour des taches brunes circulaires",
                    "Appliquer un fongicide à base de myclobutanil ou trifloxystrobine",
                    "Retirer les baies momifiées restées sur les ceps",
                    "Assurer une bonne taille pour limiter la densité du feuillage",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🫑 POIVRON (PEPPER)
    # ══════════════════════════════════════════════════════
    "pepper": {
        "name_fr": "Poivron",
        "icon": "🫑",
        "rules": [
            {
                "id": "pepper_bacterial_spot",
                "disease": "Bactériose du Poivron (Xanthomonas campestris)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 24, "humidity_min": 70,
                    "wind_min": 15,
                },
                "check": lambda w: w["temp"] >= 24 and w["humidity"] >= 70,
                "message": "Chaleur et humidité favorisent la bactériose, principale maladie du poivron.",
                "recommendations": [
                    "Traitement préventif au cuivre (bouillie bordelaise)",
                    "Éviter l'irrigation par aspersion - préférer le goutte-à-goutte",
                    "Ne pas travailler dans la culture par temps humide",
                    "Désinfecter les semences avec de l'eau chaude (50°C - 25 min)",
                    "Inspecter les fruits pour des lésions liégeuses",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🍑 PÊCHER (PEACH)
    # ══════════════════════════════════════════════════════
    "peach": {
        "name_fr": "Pêcher",
        "icon": "🍑",
        "rules": [
            {
                "id": "peach_bacterial_spot",
                "disease": "Bactériose du Pêcher (Xanthomonas arboricola)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 20, "humidity_min": 65,
                    "wind_min": 15,
                },
                "check": lambda w: w["temp"] >= 20 and w["humidity"] >= 65,
                "message": "Conditions printanières humides : risque de bactériose sur feuilles et fruits.",
                "recommendations": [
                    "Traitement au cuivre au moment de la montée de sève",
                    "Éviter les tailles par temps humide",
                    "Désinfecter les outils de taille avec de l'alcool à 70°",
                    "Inspecter les feuilles pour des taches anguleuses pourpres",
                    "Éliminer et brûler les rameaux fortement infectés",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🍓 FRAISIER (STRAWBERRY)
    # ══════════════════════════════════════════════════════
    "strawberry": {
        "name_fr": "Fraisier",
        "icon": "🍓",
        "rules": [
            {
                "id": "strawberry_leaf_scorch",
                "disease": "Brûlure des Feuilles (Xanthomonas fragariae)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 20, "humidity_min": 70,
                },
                "check": lambda w: w["temp"] >= 20 and w["humidity"] >= 70,
                "message": "Temps chaud et humide : risque de brûlure des feuilles du fraisier.",
                "recommendations": [
                    "Inspecter les feuilles pour des taches pourpres irrégulières",
                    "Éviter l'irrigation sur le feuillage",
                    "Traitement cuivrique préventif si conditions persistantes",
                    "Assurer une bonne aération entre les plantes",
                    "Éliminer les feuilles fortement infectées",
                ],
                "priority": 2,
            },
        ],
    },

    # ══════════════════════════════════════════════════════
    # 🍒 CERISIER (CHERRY)
    # ══════════════════════════════════════════════════════
    "cherry": {
        "name_fr": "Cerisier",
        "icon": "🍒",
        "rules": [
            {
                "id": "cherry_powdery_mildew",
                "disease": "Oïdium du Cerisier (Podosphaera clandestina)",
                "severity": "moderate",
                "conditions": {
                    "temp_min": 20, "humidity_min": 45,
                    "humidity_max": 70,
                },
                "check": lambda w: w["temp"] >= 20 and 45 <= w["humidity"] <= 70,
                "message": "Temps chaud et relativement sec : risque d'oïdium sur les jeunes pousses.",
                "recommendations": [
                    "Traitement au soufre mouillable (à éviter >30°C)",
                    "Inspecter les jeunes feuilles pour un feutrage blanc",
                    "Tailler pour améliorer l'aération de l'arbre",
                    "Éviter l'excès d'azote qui favorise la végétation tendre",
                ],
                "priority": 2,
            },
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# RÈGLES GLOBALES (toutes cultures confondues)
# ─────────────────────────────────────────────────────────────────────────────

GLOBAL_RULES = [
    {
        "id": "global_extreme_heat",
        "disease": "Stress Thermique — Toutes Cultures",
        "severity": "moderate",
        "cultures": ["tomato", "corn", "pepper", "potato", "strawberry"],
        "check": lambda w: w["temp"] >= 36,
        "message": "Vague de chaleur extrême : stress thermique sévère sur les cultures.",
        "recommendations": [
            "Irriguer tôt le matin ou en soirée",
            "Appliquer un paillis épais pour garder la fraîcheur du sol",
            "Éviter tout traitement chimique sous forte chaleur",
            "Surveiller l'apparition de brûlures solaires sur les fruits",
            "Utiliser des filets d'ombrage si disponibles",
        ],
        "priority": 2,
        "icon": "🌡️",
    },
    {
        "id": "global_high_humidity",
        "disease": "Risque Fongique Général — Toutes Cultures",
        "severity": "moderate",
        "cultures": ["tomato", "corn", "apple", "grape", "potato", "pepper", "peach", "strawberry", "cherry"],
        "check": lambda w: w["humidity"] >= 85,
        "message": "Humidité extrêmement élevée (≥85%) : conditions d'alerte maximale pour tous les champignons.",
        "recommendations": [
            "Traitement fongicide préventif sur toutes les cultures sensibles",
            "Améliorer la ventilation dans les serres",
            "Réduire ou suspendre l'irrigation",
            "Inspecter toutes les cultures dans les 24 prochaines heures",
        ],
        "priority": 3,
        "icon": "💧",
    },
    {
        "id": "global_strong_wind",
        "disease": "Risque de Dispersion par le Vent",
        "severity": "low",
        "cultures": ["apple", "grape", "corn"],
        "check": lambda w: w["wind"] >= 35,
        "message": "Vent fort (≥35 km/h) : dispersion accélérée des spores fongiques et des bactéries.",
        "recommendations": [
            "Suspendre tous les traitements phytosanitaires (dérive des produits)",
            "Vérifier l'état des tuteurs et attaches",
            "Inspecter les cultures après le passage du vent",
            "Planifier les traitements pour les jours calmes",
        ],
        "priority": 1,
        "icon": "🌬️",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# MOTEUR D'INFÉRENCE — Le cœur du système expert
# ─────────────────────────────────────────────────────────────────────────────

def run_expert_system(weather: Dict, farmer_cultures: Optional[List[str]] = None) -> List[Dict]:
    """
    Moteur d'inférence principal.
    
    Args:
        weather: dict avec temp, humidity, wind (données météo actuelles)
        farmer_cultures: liste des cultures de l'agriculteur (ex: ['tomato', 'grape'])
                         Si None, analyse toutes les cultures.
    
    Returns:
        Liste d'alertes générées avec recommandations, triées par priorité.
    """
    alerts = []
    
    # Sécuriser les données météo
    w = {
        "temp": float(weather.get("temp", weather.get("temperature", 20))),
        "humidity": float(weather.get("humidity", weather.get("hum", 60))),
        "wind": float(weather.get("wind", 10)),
    }

    # Déterminer les cultures à analyser
    cultures_to_check = farmer_cultures if farmer_cultures else list(EXPERT_KNOWLEDGE_BASE.keys())

    # ── 1. Appliquer les règles par culture ────────────────────────────────
    for culture_key in cultures_to_check:
        culture_key = culture_key.lower()
        if culture_key not in EXPERT_KNOWLEDGE_BASE:
            continue
        
        culture_data = EXPERT_KNOWLEDGE_BASE[culture_key]
        
        for rule in culture_data["rules"]:
            try:
                if rule["check"](w):
                    alert = _build_alert(
                        rule_id=rule["id"],
                        culture_key=culture_key,
                        culture_name=culture_data["name_fr"],
                        culture_icon=culture_data["icon"],
                        disease=rule["disease"],
                        severity=rule["severity"],
                        message=rule["message"],
                        recommendations=rule["recommendations"],
                        priority=rule["priority"],
                        weather=w,
                    )
                    alerts.append(alert)
            except Exception:
                pass

    # ── 2. Appliquer les règles globales ───────────────────────────────────
    for rule in GLOBAL_RULES:
        try:
            if rule["check"](w):
                # Filtrer selon les cultures de l'agriculteur
                concerned_cultures = rule["cultures"]
                if farmer_cultures:
                    concerned_cultures = [c for c in rule["cultures"] if c in farmer_cultures]
                
                if concerned_cultures:
                    culture_names = [EXPERT_KNOWLEDGE_BASE[c]["name_fr"] for c in concerned_cultures if c in EXPERT_KNOWLEDGE_BASE]
                    alert = {
                        "rule_id": rule["id"],
                        "culture_key": "global",
                        "culture_name": " / ".join(culture_names) if culture_names else "Toutes cultures",
                        "culture_icon": rule.get("icon", "⚠️"),
                        "disease_name": rule["disease"],
                        "severity": rule["severity"],
                        "message": rule["message"],
                        "recommendations": rule["recommendations"],
                        "priority": rule["priority"],
                        "weather_trigger": w,
                        "generated_at": datetime.now().isoformat(),
                        "type": "weather_expert",
                    }
                    alerts.append(alert)
        except Exception:
            pass

    # ── 3. Trier par priorité (3=critique, 2=modéré, 1=faible) ────────────
    alerts.sort(key=lambda x: x["priority"], reverse=True)

    # ── 4. Dédupliquer les alertes similaires ──────────────────────────────
    seen_ids = set()
    unique_alerts = []
    for alert in alerts:
        if alert["rule_id"] not in seen_ids:
            seen_ids.add(alert["rule_id"])
            unique_alerts.append(alert)

    return unique_alerts


def _build_alert(rule_id, culture_key, culture_name, culture_icon,
                  disease, severity, message, recommendations, priority, weather) -> Dict:
    """Construit un objet alerte standardisé."""
    return {
        "rule_id": rule_id,
        "culture_key": culture_key,
        "culture_name": culture_name,
        "culture_icon": culture_icon,
        "disease_name": disease,
        "severity": severity,
        "message": message,
        "recommendations": recommendations,
        "priority": priority,
        "weather_trigger": weather,
        "generated_at": datetime.now().isoformat(),
        "type": "weather_expert",
    }


def get_risk_level(weather: Dict) -> Dict:
    """
    Calcule le niveau de risque global basé sur les conditions météo.
    Retourne un résumé rapide pour le dashboard.
    """
    w = {
        "temp": float(weather.get("temp", 20)),
        "humidity": float(weather.get("humidity", weather.get("hum", 60))),
        "wind": float(weather.get("wind", 10)),
    }

    # Score de risque (0-100)
    score = 0

    # Facteur humidité (50% du score)
    if w["humidity"] >= 85: score += 50
    elif w["humidity"] >= 75: score += 35
    elif w["humidity"] >= 65: score += 20
    elif w["humidity"] >= 55: score += 10

    # Facteur température (35% du score)
    if 15 <= w["temp"] <= 25: score += 35   # Zone à risque maximal (mildiou)
    elif 25 < w["temp"] <= 32: score += 20   # Chaleur modérée
    elif w["temp"] > 36: score += 15         # Chaleur extrême (stress)
    elif w["temp"] < 10: score += 5          # Froid

    # Facteur vent (15% du score)
    if w["wind"] >= 35: score += 15
    elif w["wind"] >= 20: score += 8
    elif w["wind"] >= 10: score += 3

    # Niveau de risque
    if score >= 65:
        level = "critical"
        label = "Critique"
        color = "#f87171"
    elif score >= 40:
        level = "moderate"
        label = "Modéré"
        color = "#fbbf24"
    elif score >= 20:
        level = "low"
        label = "Faible"
        color = "#a3e635"
    else:
        level = "minimal"
        label = "Minimal"
        color = "#4ade80"

    return {
        "score": min(100, score),
        "level": level,
        "label": label,
        "color": color,
        "weather": w,
    }


def get_culture_list() -> List[Dict]:
    """Retourne la liste des cultures supportées par le système expert."""
    return [
        {"key": key, "name": data["name_fr"], "icon": data["icon"]}
        for key, data in EXPERT_KNOWLEDGE_BASE.items()
    ]


# ─────────────────────────────────────────────────────────────────────────────
# TEST RAPIDE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Simuler des conditions à risque élevé
    test_weather = {"temp": 20, "humidity": 80, "wind": 25}
    
    print("=" * 60)
    print("🌿 PhytoSentinel — Test du Système Expert")
    print("=" * 60)
    print(f"🌡️  Temp: {test_weather['temp']}°C")
    print(f"💧 Humidité: {test_weather['humidity']}%")
    print(f"🌬️  Vent: {test_weather['wind']} km/h")
    print()

    # Niveau de risque global
    risk = get_risk_level(test_weather)
    print(f"⚠️  Risque global: {risk['label']} ({risk['score']}/100)")
    print()

    # Alertes pour tomate et vigne
    alerts = run_expert_system(test_weather, farmer_cultures=["tomato", "grape", "apple"])
    print(f"🔔 {len(alerts)} alerte(s) générée(s):")
    for i, alert in enumerate(alerts, 1):
        print(f"\n  {i}. {alert['culture_icon']} [{alert['severity'].upper()}] {alert['disease_name']}")
        print(f"     📋 {alert['message']}")
        print(f"     ✅ Recommandations: {len(alert['recommendations'])}")

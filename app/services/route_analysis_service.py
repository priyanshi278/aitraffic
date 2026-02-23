def analyze_routes(routes, traffics, incidents):
    analysis = []

    for route in routes:
        route_traffic = [t for t in traffics if t["route_id"] == route["route_id"]]
        route_incidents = [i for i in incidents if i["route_id"] == route["route_id"]]

        incident_score = sum(
            3 if i["severity"] == "High"
            else 2 if i["severity"] == "Medium"
            else 1
            for i in route_incidents
        )

        congestion_level = route_traffic[0]["congestion_level"] if route_traffic else "Low"

        time_penalty = route["average_time_min"] / 10

        score = (
            incident_score +
            time_penalty +
            (3 if congestion_level == "High" else 2 if congestion_level == "Medium" else 1)
        )

        analysis.append({
            "route_id": route["route_id"],
            "via": route["via_locations"],
            "avg_time_min": route["average_time_min"],
            "incident_count": len(route_incidents),
            "congestion_level": congestion_level,
            "score": score
        })


    return analysis

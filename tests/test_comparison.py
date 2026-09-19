from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_compare_multiple_treatments():
    response = client.get(
        "/compare-multiple",
        params=[
            ("site", "Site A"),
            ("crop", "Tomato"),
            ("metric", "nitrate"),
            ("treatments", "Control"),
            ("treatments", "Treatment A"),
            ("treatments", "Treatment B"),
        ]
    )

    assert response.status_code == 200

    body = response.json()

    assert body["site"] == "Site A"
    assert body["crop"] == "Tomato"
    assert body["metric"] == "nitrate"

    assert len(body["groups"]) == 3

    treatment_names = [
        group["treatment"]
        for group in body["groups"]
    ]

    assert treatment_names == [
        "Control",
        "Treatment A",
        "Treatment B"
    ]


def test_compare_multiple_requires_two_groups():
    response = client.get(
        "/compare-multiple",
        params=[
            ("site", "Site A"),
            ("crop", "Tomato"),
            ("metric", "nitrate"),
            ("treatments", "Control"),
        ]
    )

    assert response.status_code == 400

    def test_compare_sites():
        response = client.get(
            "/compare-sites",
            params=[
                ("crop", "Tomato"),
                ("metric", "nitrate"),
                ("treatment", "Control"),
                ("sites", "Site A"),
                ("sites", "Site B"),
            ]
        )

        assert response.status_code == 200

        body = response.json()

        assert body["sites"] == [
            "Site A",
            "Site B"
        ]

        assert body["crop"] == "Tomato"
        assert body["metric"] == "nitrate"
        assert body["treatment"] == "Control"
        assert body["confidence_level"] == 0.95

        assert len(body["groups"]) == 2

        assert body["groups"][0]["site"] == "Site A"
        assert body["groups"][1]["site"] == "Site B"

        assert body["groups"][0]["n"] == 3
        assert body["groups"][1]["n"] == 3

    def test_compare_sites_requires_two_sites():
        response = client.get(
            "/compare-sites",
            params=[
                ("crop", "Tomato"),
                ("metric", "nitrate"),
                ("treatment", "Control"),
                ("sites", "Site A"),
            ]
        )

        assert response.status_code == 400

        assert response.json()["detail"] == (
            "At least two sites are required "
            "for a multi-site comparison."
        )

    def test_compare_sites_rejects_duplicate_sites():
        response = client.get(
            "/compare-sites",
            params=[
                ("crop", "Tomato"),
                ("metric", "nitrate"),
                ("treatment", "Control"),
                ("sites", "Site A"),
                ("sites", "Site A"),
            ]
        )

        assert response.status_code == 400

        assert response.json()["detail"] == (
            "Sites must be different."
        )

    def test_compare_sites_rejects_wrong_crop():
        response = client.get(
            "/compare-sites",
            params=[
                ("crop", "Maize"),
                ("metric", "nitrate"),
                ("treatment", "Control"),
                ("sites", "Site A"),
                ("sites", "Site B"),
            ]
        )

        assert response.status_code == 400
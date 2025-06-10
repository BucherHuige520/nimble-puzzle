def test_new_task(client):
    response = client.post("/task", json={
        "title": "New Task 1"
    })
    assert response.status_code == 200
    assert response.json["title"] == "New Task 1"


def test_delete_task(client):
    response = client.post("/task", json={
        "title": "Task To Delete"
    })
    assert response.status_code == 200
    assert response.json["title"] == "Task To Delete"

    # Delete it
    idx = response.json["id"]
    response = client.delete(f"/task/{idx}")
    assert response.status_code == 200
    assert response.json["title"] == "Task To Delete"

    # Not found
    response = client.get(f"/task/{idx}")
    assert response.status_code == 404


def test_update_task(client):
    # New a task for testing
    response = client.post("/task", json={
        "title": "Task which would be updated"
    })
    assert response.status_code == 200
    assert response.json["title"] == "Task which would be updated"
    assert not response.json["completed"]

    # Update it
    idx = response.json["id"]
    response = client.put(f"/task", json={
        "id": idx,
        "title": "Task Already Updated",
        "completed": True,
    })
    assert response.status_code == 200
    assert response.json["title"] == "Task Already Updated"
    assert response.json["completed"]

    # Query again
    response = client.get(f"/task/{idx}")
    assert response.status_code == 200
    assert response.json["title"] == "Task Already Updated"
    assert response.json["completed"]


def test_filter_task(client):
    tasks_per_keyword = 10
    for keyword in ["Nimble", "Web3"]:
        for i in range(tasks_per_keyword):
            response = client.post("/task", json={
                "title": f"Task {keyword} #{i}",
            })
            assert response.status_code == 200

            if i % 2 == 0:
                # Update some task
                idx = response.json["id"]
                response = client.put(f"/task", json={
                    "id": idx,
                    "completed": True,
                })
                assert response.status_code == 200

    # Filter by keyword
    response = client.get("/task/list?title=Web3")
    assert response.status_code == 200
    assert len(response.json) == tasks_per_keyword
    assert all(map(lambda x: "Web3" in x["title"], response.json)), response.json

    # Filter by keyword and completed
    response = client.get("/task/list?title=Nimble&completed=true")
    assert response.status_code == 200
    assert len(response.json) == tasks_per_keyword / 2
    assert all(map(lambda x: "Nimble" in x["title"] and x["completed"], response.json)), response.json

def test_vote_on_post(authorized_client, test_user, test_posts):
    id = test_user['id']
    post_id = test_posts[3].id
    vote = {"post_id": post_id, "dir": 1}
    r = authorized_client.post("/vote/", json = vote)
    assert r.status_code == 201
    response_msg = r.json()
    default_msg = f"Post: {post_id} liked by User: {id}"
    assert response_msg == default_msg
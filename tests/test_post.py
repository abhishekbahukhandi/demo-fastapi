import pytest
from app.anc import schema

def test_get_all_posts(authorized_client, test_posts):
    r = authorized_client.get("/posts/")
    assert r.status_code == 200
    posts = [schema.PostResponse_With_Votes(**x) for x in r.json() if x['Post']['id']==1]

def test_unauthorized_user_get_all_posts(client, test_posts):
    r = client.get("/posts/")
    assert r.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    r = client.get(f"/posts/{test_posts[0]}")
    r.status_code == 401

def test_authorized_user_get_nonexistent_post(authorized_client, test_posts):
    r = authorized_client.get(f"/posts/0")
    #print(r.json()['detail'])
    assert r.status_code == 404

def test_authorized_user_get_one_post(authorized_client, test_posts):
    r = authorized_client.get(f"/posts/{test_posts[3].id}")
    post = schema.PostResponse_With_Votes(**r.json())
    assert r.status_code == 200
    assert post.Post.id == test_posts[3].id
    assert post.Post.content == test_posts[3].content
    assert post.Post.title == test_posts[3].title
    assert post.Post.created_at == test_posts[3].created_at

@pytest.mark.parametrize('title, content, published', [
    ('New Post', 'This is new post', True),
    ('Second Post', 'This is second new post', False,),
    ('Third Post','This is third post', True,)
])
def test_create_post(authorized_client, test_user, title, content, published, test_posts):
    r = authorized_client.post("/posts/", json = {'title': title, 'content': content, 'published': published,})
    assert r.status_code == 201
    post = schema.PostResponse(**r.json())
    assert post.owner_id == test_user['id']
    assert post.title == title
    assert post.content == content
    assert post.published == published

def test_create_post_default_published(authorized_client, test_user, ):
    r = authorized_client.post("/posts/", json = {'title': 'test title', 'content': 'test content',})
    assert r.status_code == 201
    post = schema.PostResponse(**r.json())
    assert post.owner_id == test_user['id']
    assert post.title == 'test title'
    assert post.content == 'test content'
    assert post.published == True

def test_unauthorized_user_create_post(client, test_user):
    r = client.post("/posts/", json = {'title': 'New Post', 'content': 'This is new post', 'published': 'True',})
    assert r.status_code == 401

def test_authorized_deleting_post(authorized_client, test_user, test_posts):
    r = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert r.status_code == 204

def test_authorized_deleting_nonexisting_post(authorized_client, test_user, test_posts):
    r = authorized_client.delete(f"/posts/-1")
    assert r.status_code == 404
    assert r.json()['detail'] == "The requested post with id -1 does not exist"

def test_unauthorized_deleting_post(client, test_user, test_posts):
    r = client.delete(f"/posts/{test_posts[2].id}")
    assert r.status_code == 401

def test_deleting_other_users_post(authorized_client, test_posts):
    r = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert r.status_code == 403
    assert r.json()['detail'] == "Not Authorized"    

def test_update_post(authorized_client, test_posts, test_user):
    updated_data = {'title': 'Something new', 'content': 'Something really new', }
    r = authorized_client.put(f"/posts/{test_posts[0].id}", json = updated_data)
    assert r.status_code ==  200
    updated_post = schema.PostResponse(**r.json())
    assert updated_post.owner_id == test_user["id"]
    assert updated_post.title == updated_data['title']
    assert updated_post.content == updated_data['content']
    assert updated_post.id == test_posts[0].id

def test_update_other_users_post(authorized_client, test_posts):
    updated_data = {'title': 'Something new', 'content': 'Something really new', }
    r = authorized_client.put(f"/posts/{test_posts[3].id}", json = updated_data)
    assert r.status_code == 403
    assert r.json().get('detail') == "Not Authorized"

def test_update_nonexisting_post(authorized_client, test_posts):
    updated_data = {'title': 'Something new', 'content': 'Something really new', }
    r = authorized_client.put(f"/posts/0", json = updated_data)
    assert r.status_code == 404
    assert r.json().get('detail') == "Could not process the request"

def test_unauthorized_update(client, test_posts):
    updated_data = {'title': 'Something new', 'content': 'Something really new', }
    r = client.put(f"/posts/{test_posts[0].id}", json = updated_data)
    assert r.status_code == 401
    assert r.json().get('detail') == 'Not authenticated'
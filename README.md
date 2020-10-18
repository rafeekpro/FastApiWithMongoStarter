##

Simplified example of real-world-example-app *https://github.com/markqiu/fastapi-mongodb-realworld-example-app*

### Install
```
pip install -r requirements.txt
```

### Run

```
uvicorn app.main:app --reload
```

### Example data
```
{
movies: [
{
name: "The Shawshank Redemption",
casts: [
"Tim Robbins",
"Morgan Freeman",
"Bob Gunton",
"William Sadler"
],
geners: [
"Drama"
],
year: 1994,
createdAt: "2020-04-16T15:17:17Z",
slug: "the_shawshank_redemption",
classification: [
{
country: "",
value: "R"
},
{
country: "",
value: "13"
},
{
country: "",
value: "13"
}
],
id: null
},
{
name: "Avatar",
casts: [
"Sam Worthington",
"Zoe Saldaña",
"Sigourney Weaver",
"Michelle Rodríguez"
],
geners: [
"Science Fiction",
"Action"
],
year: 2009,
createdAt: "2020-10-17T16:58:05Z",
slug: "avatar",
classification: [
{
country: "",
value: "PG-13"
},
{
country: "",
value: "+13"
},
{
country: "",
value: "+7"
},
{
country: "",
value: "+12"
}
],
id: null
}
],
moviesCount: 2
}
```
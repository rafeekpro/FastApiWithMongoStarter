// Initialize MongoDB with sample data
db = db.getSiblingDB('fastapi');

// Create user for the application
db.createUser({
  user: 'admin',
  pwd: 'admin123',
  roles: [
    {
      role: 'readWrite',
      db: 'fastapi'
    }
  ]
});

// Create movies collection with sample data
db.createCollection('movies');

db.movies.insertMany([
  {
    name: "The Shawshank Redemption",
    casts: ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
    genres: ["Drama"],
    year: 1994,
    slug: "the-shawshank-redemption",
    classification: [
      { country: "US", value: "R" },
      { country: "UK", value: "15" },
      { country: "DE", value: "12" }
    ],
    created_at: new Date("2024-01-01T00:00:00Z"),
    updated_at: null
  },
  {
    name: "The Godfather",
    casts: ["Marlon Brando", "Al Pacino", "James Caan", "Robert Duvall"],
    genres: ["Crime", "Drama"],
    year: 1972,
    slug: "the-godfather",
    classification: [
      { country: "US", value: "R" },
      { country: "UK", value: "18" }
    ],
    created_at: new Date("2024-01-01T00:00:00Z"),
    updated_at: null
  },
  {
    name: "The Dark Knight",
    casts: ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine"],
    genres: ["Action", "Crime", "Drama"],
    year: 2008,
    slug: "the-dark-knight",
    classification: [
      { country: "US", value: "PG-13" },
      { country: "UK", value: "12A" }
    ],
    created_at: new Date("2024-01-01T00:00:00Z"),
    updated_at: null
  },
  {
    name: "Pulp Fiction",
    casts: ["John Travolta", "Uma Thurman", "Samuel L. Jackson", "Bruce Willis"],
    genres: ["Crime", "Drama"],
    year: 1994,
    slug: "pulp-fiction",
    classification: [
      { country: "US", value: "R" },
      { country: "UK", value: "18" }
    ],
    created_at: new Date("2024-01-01T00:00:00Z"),
    updated_at: null
  },
  {
    name: "Inception",
    casts: ["Leonardo DiCaprio", "Marion Cotillard", "Elliot Page", "Tom Hardy"],
    genres: ["Action", "Science Fiction", "Thriller"],
    year: 2010,
    slug: "inception",
    classification: [
      { country: "US", value: "PG-13" },
      { country: "UK", value: "12A" }
    ],
    created_at: new Date("2024-01-01T00:00:00Z"),
    updated_at: null
  }
]);

// Create indexes for better performance
db.movies.createIndex({ slug: 1 }, { unique: true });
db.movies.createIndex({ name: "text" });
db.movies.createIndex({ year: 1 });
db.movies.createIndex({ genres: 1 });

print('MongoDB initialized with sample data');
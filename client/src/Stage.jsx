import { useGame } from "@empirica/core/player/classic/react";
import { Loading } from "@empirica/core/player/react";
import React from "react";

export function Stage() {
  const game = useGame();
  const scenario = game.get("scenario");
  const showIdentities = import.meta.env.VITE_SHOW_IDENTITIES !== "false";

  if (!scenario) return <Loading />;

  return (
    <main className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold">Agentic RecSys Arena</h1>
      {showIdentities && <p className="mt-3">MovieLens user ID: {scenario.userId}</p>}
      {Object.entries(scenario.recommendations).map(([model, movies], index) => (
        <section className="mt-8" key={model}>
          <h2 className="text-2xl font-semibold">{showIdentities ? model : `List ${index + 1}`}</h2>
          <ol className="mt-3 list-decimal pl-6">
            {movies.map((movie) => (
              <li className="mb-2" key={movie.movieId}>
                {movie.title} ({movie.year})
                {movie.genres.length > 0 && <span className="ml-2 text-gray-600">{movie.genres.join(", ")}</span>}
              </li>
            ))}
          </ol>
        </section>
      ))}
    </main>
  );
}

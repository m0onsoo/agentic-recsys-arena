import { usePlayer } from "@empirica/core/player/classic/react";
import { Loading } from "@empirica/core/player/react";
import React from "react";

export function Stage() {
  const player = usePlayer();

  if (player.stage.get("submit")) {
    return <Loading />;
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center gap-6 px-6 py-12">
      <h1 className="text-3xl font-semibold">Agentic RecSys Arena</h1>
      <p>
        Empirica is running. This setup check contains no recommendation
        scenarios and does not collect a research judgment.
      </p>
      <button
        className="w-fit rounded bg-blue-700 px-5 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-400"
        onClick={() => player.stage.set("submit", true)}
        type="button"
      >
        Complete setup check
      </button>
    </main>
  );
}

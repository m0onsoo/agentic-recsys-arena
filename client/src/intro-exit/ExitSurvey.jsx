import React from "react";
import { Button } from "../components/Button";

export function ExitSurvey({ next }) {
  return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="text-3xl font-semibold">Setup check complete</h1>
      <p className="my-6">No research judgment was collected.</p>
      <Button handleClick={next}>Finish</Button>
    </main>
  );
}

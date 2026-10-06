import React from "react";
import { Button } from "../components/Button";

export function Introduction({ next }) {
  return (
    <div className="mx-auto max-w-2xl px-6 py-12">
      <h1 className="text-3xl font-semibold">Agentic RecSys Arena</h1>
      <p className="my-6">
        This is a technical setup check. No recommendation scenarios are available
        yet, and no research judgment will be collected.
      </p>
      <Button handleClick={next} autoFocus>
        Continue
      </Button>
    </div>
  );
}

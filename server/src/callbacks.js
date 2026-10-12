import { ClassicListenersCollector } from "@empirica/core/admin/classic";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
export const Empirica = new ClassicListenersCollector();

Empirica.onGameStart(({ game }) => {
  const python = process.env.ARA_PYTHON || "python3";
  const userId = process.env.ARA_USER_ID || "1080";
  const script = join(__dirname, "..", "..", "scripts", "recommend.py");
  const result = execFileSync(python, [script, "--user-id", userId], {
    encoding: "utf8",
    timeout: 120000,
  });
  game.set("scenario", JSON.parse(result));
  const round = game.addRound({ name: "Recommendations", task: "recommendations" });
  round.addStage({ name: "Browse", duration: 300 });
});

Empirica.onRoundStart(({ round }) => {});

Empirica.onStageStart(({ stage }) => {});

Empirica.onStageEnded(({ stage }) => {});

Empirica.onRoundEnded(({ round }) => {});

Empirica.onGameEnded(({ game }) => {});

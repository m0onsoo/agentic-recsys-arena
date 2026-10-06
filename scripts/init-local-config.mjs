import { randomBytes } from "node:crypto";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../.empirica/", import.meta.url));
const configPath = `${root}empirica.toml`;
const idPath = `${root}id`;

if (existsSync(configPath) || existsSync(idPath)) {
  console.error("Local Empirica configuration already exists; no files changed.");
  process.exitCode = 1;
} else {
  const token = randomBytes(24).toString("hex");
  const password = randomBytes(18).toString("hex");
  const id = randomBytes(8).toString("hex");
  const config = `name = "ARA"\n\n[tajriba.auth]\nsrtoken = "${token}"\n\n[[tajriba.auth.users]]\nname = "Admin"\nusername = "admin"\npassword = "${password}"\n`;

  mkdirSync(`${root}local`, { recursive: true });
  writeFileSync(configPath, config, { mode: 0o600, flag: "wx" });
  writeFileSync(idPath, id, { mode: 0o600, flag: "wx" });
  console.log("Created local Empirica configuration. Read credentials from .empirica/empirica.toml.");
}

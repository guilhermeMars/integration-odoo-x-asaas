import express from "express";
import config from "./config/index.js";
import invoiceRoutes from "./routes/cobrancaRoutes.js";
import umblerRoutes from "./routes/umblerRoutes.js";

const app = express();

app.use(express.json());
app.use("/", invoiceRoutes);
app.use("/umbler", umblerRoutes);

app.listen(config.port, () => {
  console.log(`Server running on http://localhost:${config.port}`);
});

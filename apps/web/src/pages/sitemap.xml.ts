import publicCatalog from "../data/catalog.public.json";

const staticRoutes = [
  "/",
  "/guias/",
  "/guias/margem-vs-markup-como-calcular-preco-de-venda/",
  "/guias/quanto-custa-dar-10-por-cento-de-desconto/",
];

export async function GET({ site }: { site?: URL }) {
  const baseUrl = (site?.toString() || "https://prismadados.pages.dev").replace(/\/$/, "");

  const productRoutes = publicCatalog
    .filter((item) => item.status === "live")
    .map((item) => `/p/${item.slug}/`);

  const allRoutes = [...staticRoutes, ...productRoutes];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allRoutes
  .map(
    (route) => `  <url>
    <loc>${baseUrl}${route}</loc>
    <changefreq>weekly</changefreq>
  </url>`
  )
  .join("\n")}
</urlset>
`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
    },
  });
}

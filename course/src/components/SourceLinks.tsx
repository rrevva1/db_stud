import type { Source, SourceRef, SourcesCatalog } from "../types";

interface SourceLinksProps {
  required: SourceRef[];
  optional: SourceRef[];
  sources: SourcesCatalog;
}

function queueLabel(index: number): string {
  return `${index + 1}-я очередь`;
}

function sourceHeading(src: Source | undefined, fallbackId: string): string {
  if (!src) return fallbackId;
  return src.authors ? `${src.authors} — ${src.title}` : src.title;
}

export default function SourceLinks({
  required,
  optional,
  sources,
}: SourceLinksProps) {
  const resolve = (ref: SourceRef) =>
    sources.sources.find((s) => s.id === ref.sourceId);

  return (
    <section className="sources-block">
      <h2>Источники для изучения</h2>
      <p className="sources-note">
        Читайте в указанной очереди. Текст книг в урок не включён — открывайте
        оригинал по пути в папке <code>sources/</code>.
      </p>
      {required.length > 0 && (
        <>
          <h3>Очередь чтения</h3>
          <ol className="sources-list sources-queue">
            {required.map((r, i) => {
              const src = resolve(r);
              return (
                <li key={`${r.sourceId}-${i}`}>
                  <span className="queue-label">{queueLabel(i)}</span>
                  <strong>{sourceHeading(src, r.sourceId)}</strong>
                  <br />
                  <span className="ref">{r.ref}</span>
                  {src?.path && (
                    <>
                      <br />
                      <code className="path">{src.path}</code>
                    </>
                  )}
                </li>
              );
            })}
          </ol>
        </>
      )}
      {optional.length > 0 && (
        <>
          <h3>Далее (по желанию)</h3>
          <ul className="sources-list optional">
            {optional.map((r, i) => {
              const src = resolve(r);
              return (
                <li key={`${r.sourceId}-${i}`}>
                  <strong>{sourceHeading(src, r.sourceId)}</strong>
                  <br />
                  <span className="ref">{r.ref}</span>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </section>
  );
}

import { marked } from "marked";

interface TasksProps {
  markdown: string;
}

export default function TasksBlock({ markdown }: TasksProps) {
  if (!markdown.trim()) return null;
  const html = marked.parse(markdown) as string;
  return (
    <section className="tasks-block">
      <h2>Практические задания</h2>
      <div
        className="markdown tasks-content"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </section>
  );
}

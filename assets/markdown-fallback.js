(function () {
  'use strict';

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function safeHref(value) {
    const href = String(value || '').trim();
    if (/^(https?:\/\/|#|\.\.?\/|[A-Za-z0-9_./-]+(?:\?[^\s]*)?)$/i.test(href)) {
      return escapeHtml(href);
    }
    return '#';
  }

  function inlineMarkdown(value) {
    const codeTokens = [];
    let text = String(value).replace(/`([^`]+)`/g, function (_match, code) {
      const token = '@@CODE' + codeTokens.length + '@@';
      codeTokens.push('<code>' + escapeHtml(code) + '</code>');
      return token;
    });

    text = escapeHtml(text);
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, function (_match, label, href) {
      return '<a href="' + safeHref(href) + '">' + label + '</a>';
    });
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/__([^_]+)__/g, '<strong>$1</strong>');
    text = text.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
    text = text.replace(/(^|[^_])_([^_\n]+)_(?!_)/g, '$1<em>$2</em>');
    text = text.replace(/  $/, '<br>');

    codeTokens.forEach(function (html, index) {
      text = text.replace('@@CODE' + index + '@@', html);
    });
    return text;
  }

  function splitTableRow(line) {
    let row = line.trim();
    if (row.startsWith('|')) row = row.slice(1);
    if (row.endsWith('|')) row = row.slice(0, -1);
    return row.split('|').map(function (cell) { return cell.trim(); });
  }

  function isTableSeparator(line) {
    const cells = splitTableRow(line);
    return cells.length > 0 && cells.every(function (cell) {
      return /^:?-{3,}:?$/.test(cell);
    });
  }

  function basicMarkdown(md) {
    const lines = String(md || '').replace(/\r\n?/g, '\n').split('\n');
    const html = [];
    let i = 0;
    let paragraph = [];

    function flushParagraph() {
      if (!paragraph.length) return;
      html.push('<p>' + paragraph.map(inlineMarkdown).join(' ') + '</p>');
      paragraph = [];
    }

    while (i < lines.length) {
      const line = lines[i];
      const trimmed = line.trim();

      if (/^```/.test(trimmed)) {
        flushParagraph();
        const language = trimmed.slice(3).trim();
        const code = [];
        i += 1;
        while (i < lines.length && !/^```/.test(lines[i].trim())) {
          code.push(lines[i]);
          i += 1;
        }
        const className = language ? ' class="language-' + escapeHtml(language) + '"' : '';
        html.push('<pre><code' + className + '>' + escapeHtml(code.join('\n')) + '</code></pre>');
        i += 1;
        continue;
      }

      if (!trimmed) {
        flushParagraph();
        i += 1;
        continue;
      }

      const heading = /^(#{1,6})\s+(.+)$/.exec(trimmed);
      if (heading) {
        flushParagraph();
        const level = heading[1].length;
        html.push('<h' + level + '>' + inlineMarkdown(heading[2]) + '</h' + level + '>');
        i += 1;
        continue;
      }

      if (/^(?:-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
        flushParagraph();
        html.push('<hr>');
        i += 1;
        continue;
      }

      if (trimmed.startsWith('>')) {
        flushParagraph();
        const quote = [];
        while (i < lines.length && lines[i].trim().startsWith('>')) {
          quote.push(lines[i].trim().replace(/^>\s?/, ''));
          i += 1;
        }
        html.push('<blockquote><p>' + quote.map(inlineMarkdown).join('<br>') + '</p></blockquote>');
        continue;
      }

      if (i + 1 < lines.length && trimmed.includes('|') && isTableSeparator(lines[i + 1])) {
        flushParagraph();
        const headers = splitTableRow(line);
        i += 2;
        const rows = [];
        while (i < lines.length && lines[i].trim() && lines[i].includes('|')) {
          rows.push(splitTableRow(lines[i]));
          i += 1;
        }
        html.push('<table><thead><tr>' + headers.map(function (cell) {
          return '<th>' + inlineMarkdown(cell) + '</th>';
        }).join('') + '</tr></thead><tbody>' + rows.map(function (row) {
          return '<tr>' + row.map(function (cell) {
            return '<td>' + inlineMarkdown(cell) + '</td>';
          }).join('') + '</tr>';
        }).join('') + '</tbody></table>');
        continue;
      }

      if (/^[-+*]\s+/.test(trimmed)) {
        flushParagraph();
        const items = [];
        while (i < lines.length && /^[-+*]\s+/.test(lines[i].trim())) {
          items.push(lines[i].trim().replace(/^[-+*]\s+/, ''));
          i += 1;
        }
        html.push('<ul>' + items.map(function (item) {
          return '<li>' + inlineMarkdown(item) + '</li>';
        }).join('') + '</ul>');
        continue;
      }

      if (/^\d+[.)]\s+/.test(trimmed)) {
        flushParagraph();
        const items = [];
        while (i < lines.length && /^\d+[.)]\s+/.test(lines[i].trim())) {
          items.push(lines[i].trim().replace(/^\d+[.)]\s+/, ''));
          i += 1;
        }
        html.push('<ol>' + items.map(function (item) {
          return '<li>' + inlineMarkdown(item) + '</li>';
        }).join('') + '</ol>');
        continue;
      }

      paragraph.push(trimmed);
      i += 1;
    }

    flushParagraph();
    return html.join('\n');
  }

  window.renderReportMarkdown = function (markdown) {
    if (window.marked && typeof window.marked.parse === 'function') {
      return window.marked.parse(markdown);
    }
    return basicMarkdown(markdown);
  };
})();

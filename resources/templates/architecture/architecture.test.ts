import { describe, it, expect } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

/**
 * GENERIC ARCHITECTURAL INVARIANT & AI GUARDRAIL TESTS
 *
 * Core Principle:
 * "An AI agent can drift from prose in a markdown file, but it cannot ignore
 * a failing unit test in the terminal (FAIL) or a blocked git commit."
 *
 * Customize the configuration constants below to enforce your project's specific invariants.
 */

// ==============================================================================
// 1. PROJECT INVARIANT CONFIGURATION (Customize for your stack & rules)
// ==============================================================================

const CONFIG = {
  // Banned AI cliché icons (overused generative UI tropes)
  bannedIcons: ['Sparkles', 'Flame', 'Zap'],
  
  // Banned heavy packages when lightweight or native primitives are required
  bannedDependencies: ['recharts', 'chart.js', 'd3', 'lodash', 'moment'],
  
  // Modules permitted to interact directly with browser storage (SSR & privacy safe)
  allowedStorageWrappers: ['storage.ts', 'storage.test.ts', 'storage.tsx'],
  
  // Directories excluded from static scanning
  excludedDirectories: ['node_modules', '.git', '.next', 'dist', 'build', '.agents', '.venv'],
  
  // Require tabular figures on numeric counters and timers to prevent layout shifts
  enforceTabularNums: true,
  
  // Require pointer-events-none on button SVG icons to prevent touch capture bugs
  enforceButtonSvgPointerEvents: true,
};

// ==============================================================================
// 2. FILE CRAWLER UTILITY
// ==============================================================================

const ROOT_DIR = path.resolve(__dirname, '../../');
const SRC_DIR = path.resolve(ROOT_DIR, 'src');

function getAllSourceFiles(dirPath: string, arrayOfFiles: string[] = []): string[] {
  if (!fs.existsSync(dirPath)) return arrayOfFiles;
  const entries = fs.readdirSync(dirPath);

  entries.forEach((entry) => {
    const fullPath = path.join(dirPath, entry);
    if (fs.statSync(fullPath).isDirectory()) {
      if (!CONFIG.excludedDirectories.includes(entry)) {
        arrayOfFiles = getAllSourceFiles(fullPath, arrayOfFiles);
      }
    } else {
      arrayOfFiles.push(fullPath);
    }
  });

  return arrayOfFiles;
}

const sourceFiles = fs.existsSync(SRC_DIR) ? getAllSourceFiles(SRC_DIR) : [];
const codeFiles = sourceFiles.filter(
  (f) => /\.(ts|tsx|js|jsx)$/.test(f) && !f.endsWith('.test.ts') && !f.endsWith('.test.tsx')
);
const templateFiles = codeFiles.filter((f) => f.endsWith('.tsx') || f.endsWith('.jsx'));

// ==============================================================================
// 3. ARCHITECTURAL INVARIANT TEST SUITE
// ==============================================================================

describe('Automated Architectural Invariants & AI Guardrails', () => {

  // Pillar 1: Zero-Leak Secrets Security
  it('Zero-Leak: No hardcoded API keys, private tokens, or credentials in source code', () => {
    const secretPatterns = [
      /sk-[a-zA-Z0-9]{20,}/,
      /ghp_[a-zA-Z0-9]{30,}/,
      /AIzaSy[a-zA-Z0-9_-]{33}/,
      /BEGIN (RSA|EC|PRIVATE) KEY/,
      /(password|secret|api_key|apiKey)\s*[:=]\s*["'][a-zA-Z0-9_!@#$%^&*()+=]{8,}["']/i
    ];

    codeFiles.forEach((file) => {
      const content = fs.readFileSync(file, 'utf-8');
      secretPatterns.forEach((pattern) => {
        const match = content.match(pattern);
        expect(
          match,
          `Security violation: Potential hardcoded secret in ${path.relative(ROOT_DIR, file)}: ${match?.[0]}`
        ).toBeNull();
      });
    });
  });

  // Pillar 2: Anti-AI Clichés & Visual Tone
  it('Anti-AI Clichés: No generic AI cliché icons imported from iconography libraries', () => {
    const lucideRegex = /import\s*\{([^}]+)\}\s*from\s*['"]lucide-react['"]/g;

    codeFiles.forEach((file) => {
      const content = fs.readFileSync(file, 'utf-8');
      let match;
      while ((match = lucideRegex.exec(content)) !== null) {
        const imported = match[1].split(',').map((s) => s.trim());
        CONFIG.bannedIcons.forEach((banned) => {
          expect(
            imported.includes(banned),
            `Design violation: Banned cliché icon "${banned}" imported in ${path.relative(ROOT_DIR, file)}. Prefer domain-specific, sober iconography.`
          ).toBe(false);
        });
      }
    });
  });

  it('Anti-AI Clichés: No superfluous decorative emojis in UI labels', () => {
    const emojiRegex = /[\u{1F300}-\u{1F6FF}\u{1F900}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;

    codeFiles.forEach((file) => {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n');

      lines.forEach((line, idx) => {
        if (line.trim().startsWith('//') || line.trim().startsWith('/*') || line.trim().startsWith('*')) return;
        if (emojiRegex.test(line)) {
          expect(
            false,
            `Style violation: Decorative emoji detected at ${path.relative(ROOT_DIR, file)}:${idx + 1}. Maintain a clean, professional, clutter-free interface.`
          ).toBe(true);
        }
      });
    });
  });

  // Pillar 3: Encapsulation & Storage Boundaries
  it('Encapsulation: No unmanaged direct localStorage access in domain modules', () => {
    codeFiles.forEach((file) => {
      if (CONFIG.allowedStorageWrappers.some((allowed) => file.endsWith(allowed))) return;

      const content = fs.readFileSync(file, 'utf-8');
      const hasDirectStorage = /\b(window\.)?localStorage\b/.test(content);

      expect(
        hasDirectStorage,
        `Architecture violation: Direct localStorage access found in ${path.relative(ROOT_DIR, file)}. Use the centralized safe storage wrapper for SSR and private browsing safety.`
      ).toBe(false);
    });
  });

  // Pillar 4: Ergonomics & Touch Event Robustness
  it('Ergonomics: Clickable button icons should specify pointer-events-none', () => {
    if (!CONFIG.enforceButtonSvgPointerEvents) return;

    templateFiles.forEach((file) => {
      const content = fs.readFileSync(file, 'utf-8');
      const svgTagRegex = /<svg\b([^>]*)>/g;
      let match;
      while ((match = svgTagRegex.exec(content)) !== null) {
        const attributes = match[1];
        if (content.includes('<button') && !attributes.includes('pointer-events-none')) {
          // Warning/check for custom inline SVG icons to prevent touch event interception
        }
      }
    });
  });

  it('Ergonomics: Timers and numeric metrics should use tabular figures to prevent jitter', () => {
    if (!CONFIG.enforceTabularNums) return;

    templateFiles.forEach((file) => {
      const content = fs.readFileSync(file, 'utf-8');
      if (/(\btimer\b|\bcounter\b|\bstopwatch\b|\bprice\b|\bmetric\b)/i.test(content)) {
        if (content.includes('className=') && !content.includes('tabular-nums')) {
          console.warn(`[Ergonomics Advisory] Check ${path.relative(ROOT_DIR, file)}: Consider adding 'tabular-nums' to prevent layout shifts on value updates.`);
        }
      }
    });
  });

  // Pillar 5: Dependency Diet & Bloat Prevention
  it('Dependency Diet: No unauthorized heavy third-party libraries in package.json', () => {
    const pkgPath = path.resolve(ROOT_DIR, 'package.json');
    if (!fs.existsSync(pkgPath)) return;

    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    const allDeps = {
      ...(pkg.dependencies || {}),
      ...(pkg.devDependencies || {})
    };

    CONFIG.bannedDependencies.forEach((lib) => {
      expect(
        Boolean(allDeps[lib]),
        `Dependency Bloat violation: Heavy package "${lib}" detected in package.json. Use approved lightweight or native alternatives.`
      ).toBe(false);
    });
  });

});

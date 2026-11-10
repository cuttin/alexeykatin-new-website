import { getCollection } from 'astro:content';

// Photos of each post, keyed by post id (folder name), in file-name order (01.jpg, 02.jpg, ...).
const files = import.meta.glob('/src/content/memories/*/*.{jpg,jpeg,png,gif}', { eager: true, import: 'default' });
const photos = {};
for (const [path, img] of Object.entries(files).sort(([a], [b]) => a.localeCompare(b))) {
  (photos[path.split('/').at(-2)] ??= []).push(img);
}

export const CATS = ['Япония', 'Азия', 'США', 'Полезное'];
const MONTHS = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь'];
const MONTHS_GEN = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
export const month = (d) => MONTHS[d.getUTCMonth()];
export const longDate = (d) => `${d.getUTCDate()} ${MONTHS_GEN[d.getUTCMonth()]} ${d.getUTCFullYear()}`;

// Russian plural for "фото" is invariable; kept as a function in case the wording changes.
export const photoCount = (n) => `${n} фото`;

// Newest first.
export async function allMemories() {
  const posts = await getCollection('memories');
  return posts
    .sort((a, b) => b.data.date - a.data.date)
    .map((p) => ({ ...p, photos: photos[p.id] ?? [] }));
}

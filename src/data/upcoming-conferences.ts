// Prochaines conférences à afficher sur la page d'accueil.
// Ajoutez ou retirez des entrées ici au fil des événements programmés.
export interface UpcomingConference {
  title: string;
  date: Date;
  summary: string;
  bookingUrl: string;
}

export const upcomingConferences: UpcomingConference[] = [
  {
    title: "Comment fonctionne une plate-forme d'agents IA",
    date: new Date('2026-10-15'),
    summary:
      "Panorama concret des briques qui composent une plateforme d'agents IA : orchestration, outils, mémoire et supervision.",
    bookingUrl: 'mailto:ai.referent@gmail.com?subject=Inscription%20-%20Plate-forme%20d%27agents%20IA',
  },
  {
    title: 'Introduction aux embeddings de position',
    date: new Date('2026-11-12'),
    summary:
      "Comprendre le rôle des embeddings de position dans les modèles de langage, de l'encodage sinusoïdal aux approches les plus récentes.",
    bookingUrl: 'mailto:ai.referent@gmail.com?subject=Inscription%20-%20Embeddings%20de%20position',
  },
];

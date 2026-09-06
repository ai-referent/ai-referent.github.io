// Prochaines conférences à afficher sur la page d'accueil.
// Ajoutez ou retirez des entrées ici au fil des événements programmés.
export interface UpcomingConference {
  title: string;
  date: Date;
  summary: string;
  bookingUrl: string;
}

export const upcomingConferences: UpcomingConference[] = [];

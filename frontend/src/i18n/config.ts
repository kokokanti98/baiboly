import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import mgTranslation from './mg/translation.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      mg: {
        translation: mgTranslation,
      },
    },
    lng: 'mg', // Default language: Malagasy
    fallbackLng: 'mg',
    interpolation: {
      escapeValue: false, // React already escapes
    },
  });

export default i18n;

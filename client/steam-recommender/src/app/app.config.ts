import { ApplicationConfig, Component, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { definePreset } from '@primeng/themes';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { providePrimeNG } from "primeng/config"
import Lara from '@primeuix/themes/lara';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ 
      eventCoalescing: true 
    }), 
    provideRouter(routes),
    provideHttpClient(),
    provideAnimationsAsync(),
    providePrimeNG({
      theme: {
          preset: definePreset(Lara, {
            semantic: {
              primary: {
                  50: '{slate.50}',
                  100: '{slate.100}',
                  200: '{slate.200}',
                  300: '{slate.300}',
                  400: '{slate.400}',
                  500: '{slate.500}',
                  600: '{slate.600}',
                  700: '{slate.700}',
                  800: '{slate.800}',
                  900: '{slate.900}',
                  950: '{slate.950}'
              },
              colorScheme: {
                light: {
                  primary: {
                    color: '{zinc.950}',
                    inverseColor: '#ffffff',
                    hoverColor: '{zinc.900}',
                    activeColor: '{zinc.800}'
                  },
                  highlight: {
                    background: '{purple.950}',
                    focusBackground: '{zinc.700}',
                    color: '#ffffff',
                    focusColor: '#ffffff'
                  }
                },
                dark: {
                  primary: {
                    color: '{zinc.50}',
                    inverseColor: '{zinc.950}',
                    hoverColor: '{zinc.100}',
                    activeColor: '{zinc.200}'
                  },
                  highlight: {
                    background: 'rgba(250, 250, 250, .16)',
                    focusBackground: 'rgba(250, 250, 250, .24)',
                    color: 'rgba(255,255,255,.87)',
                    focusColor: 'rgba(255,255,255,.87)'
                  }
                }
              }
            }
          }),
          options: {
              darkModeSelector: false || 'none'
          }
      },
    })
  ]
};

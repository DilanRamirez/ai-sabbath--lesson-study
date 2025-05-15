import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { BookOpenText, Users, CalendarDays } from "lucide-react";

export default function HomePage() {
  return (
    <div className="flex flex-col items-center">
      {/* Hero Section */}
      <section className="relative w-full bg-muted text-center py-20 md:py-32 lg:py-40">
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
          style={{ backgroundImage: `url('/your-banner.jpg')` }}
        ></div>
        <div className="relative z-10 max-w-3xl mx-auto px-4">
          <h1 className="text-3xl md:text-5xl font-bold text-foreground mb-4">
            Bienvenido a tu Escuela Sabática Interactiva
          </h1>
          <p className="text-muted-foreground text-lg">
            Profundiza tu estudio bíblico diario con herramientas interactivas y reflexiones personales.
          </p>
        </div>
      </section>

      {/* Main Actions */}
      <section className="w-full py-12 md:py-24 lg:py-32 bg-background">
        <div className="container px-4 md:px-6">
          <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-3 lg:gap-12">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="rounded-full p-4 bg-primary/10">
                <CalendarDays className="h-10 w-10 text-primary" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Comenzar Lección de Hoy</h3>
                <p className="text-muted-foreground">Continúa tu estudio diario con la lección de hoy.</p>
              </div>
              <Button asChild size="lg" className="mt-4">
                <Link href="/lesson/current">Comenzar Ahora</Link>
              </Button>
            </div>
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="rounded-full p-4 bg-primary/10">
                <BookOpenText className="h-10 w-10 text-primary" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Ver Todas las Lecciones</h3>
                <p className="text-muted-foreground">Explora todas las lecciones disponibles por trimestre.</p>
              </div>
              <Button asChild size="lg" className="mt-4">
                <Link href="/lessons">Ver Lecciones</Link>
              </Button>
            </div>
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="rounded-full p-4 bg-primary/10">
                <Users className="h-10 w-10 text-primary" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Unirse a un Grupo de Estudio</h3>
                <p className="text-muted-foreground">Conéctate con otros estudiantes y maestros.</p>
              </div>
              <Button asChild size="lg" className="mt-4">
                <Link href="/groups/join">Unirse a Grupo</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

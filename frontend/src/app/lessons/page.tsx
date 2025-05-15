import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

// Mock data for lessons
const adultLessons = [
  {
    id: 1,
    title: "El Mensaje de Hebreos",
    coverImage: "/placeholder.svg?height=300&width=200",
    dateRange: "Enero - Marzo 2024",
    progress: 50,
    completedDays: 3,
    totalDays: 6,
    currentWeek: "Semana 6: Mayo 4–10",
    isCurrentTrimester: true,
  },
  {
    id: 2,
    title: "La Fe de Jesús",
    coverImage: "/placeholder.svg?height=300&width=200",
    dateRange: "Abril - Junio 2024",
    progress: 0,
    completedDays: 0,
    totalDays: 6,
    currentWeek: "Semana 1: Abril 1–7",
    isCurrentTrimester: false,
  },
];

const inverseLessons = [
  {
    id: 3,
    title: "InVerse: Discipulado",
    coverImage: "/placeholder.svg?height=300&width=200",
    dateRange: "Enero - Marzo 2024",
    progress: 83,
    completedDays: 5,
    totalDays: 6,
    currentWeek: "Semana 6: Mayo 4–10",
    isCurrentTrimester: true,
  },
];

export default function LessonsPage() {
  return (
    <div className="container py-8">
      <h1 className="text-3xl font-bold mb-8">Lecciones de Escuela Sabática</h1>

      <Tabs defaultValue="adult" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2 mb-8">
          <TabsTrigger value="adult">Edición para Adultos</TabsTrigger>
          <TabsTrigger value="inverse">InVerse</TabsTrigger>
        </TabsList>

        <TabsContent value="adult" className="space-y-8">
          <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
            {adultLessons.map((lesson) => (
              <Card key={lesson.id} className={lesson.isCurrentTrimester ? "border-primary" : ""}>
                <CardHeader className="p-0">
                  <div className="relative h-48 w-full">
                    <Image
                      src={lesson.coverImage || "/placeholder.svg"}
                      alt={lesson.title}
                      fill
                      className="object-cover rounded-t-lg"
                    />
                    {lesson.isCurrentTrimester && <Badge className="absolute top-2 right-2">Actual</Badge>}
                  </div>
                </CardHeader>
                <CardContent className="p-6">
                  <CardTitle className="mb-2">{lesson.title}</CardTitle>
                  <p className="text-sm text-muted-foreground mb-2">{lesson.dateRange}</p>
                  <p className="text-sm font-medium mb-2">{lesson.currentWeek}</p>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progreso</span>
                      <span>
                        {lesson.completedDays}/{lesson.totalDays} días completados
                      </span>
                    </div>
                    <Progress value={lesson.progress} className="h-2" />
                  </div>
                </CardContent>
                <CardFooter>
                  <Link
                    href={`/lesson/${lesson.id}/1`}
                    className="w-full inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                  >
                    {lesson.progress > 0 ? "Continuar Estudio" : "Comenzar Estudio"}
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="inverse" className="space-y-8">
          <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
            {inverseLessons.map((lesson) => (
              <Card key={lesson.id} className={lesson.isCurrentTrimester ? "border-primary" : ""}>
                <CardHeader className="p-0">
                  <div className="relative h-48 w-full">
                    <Image
                      src={lesson.coverImage || "/placeholder.svg"}
                      alt={lesson.title}
                      fill
                      className="object-cover rounded-t-lg"
                    />
                    {lesson.isCurrentTrimester && <Badge className="absolute top-2 right-2">Actual</Badge>}
                  </div>
                </CardHeader>
                <CardContent className="p-6">
                  <CardTitle className="mb-2">{lesson.title}</CardTitle>
                  <p className="text-sm text-muted-foreground mb-2">{lesson.dateRange}</p>
                  <p className="text-sm font-medium mb-2">{lesson.currentWeek}</p>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progreso</span>
                      <span>
                        {lesson.completedDays}/{lesson.totalDays} días completados
                      </span>
                    </div>
                    <Progress value={lesson.progress} className="h-2" />
                  </div>
                </CardContent>
                <CardFooter>
                  <Link
                    href={`/lesson/${lesson.id}/1`}
                    className="w-full inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                  >
                    {lesson.progress > 0 ? "Continuar Estudio" : "Comenzar Estudio"}
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

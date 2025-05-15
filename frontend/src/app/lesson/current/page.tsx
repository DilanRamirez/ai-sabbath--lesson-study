"use client";

import React from "react";
import { useState } from "react";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { AccessibilityIcon as PsychologyAlt, BookOpen, Check, Share2 } from "lucide-react";

// Mock data for a lesson day
const lessonData = {
  title: "El Mensaje de Hebreos",
  dayTitle: "El Mensaje de Hebreos",
  subtitle: "Domingo, 5 de Mayo, 2024",
  bannerImage: "/placeholder.svg?height=400&width=1200",
  content: [
    {
      type: "paragraph",
      text: "La carta a los Hebreos comienza sin las presentaciones típicas que caracterizan las epístolas antiguas. En lugar de seguir la costumbre de identificarse a sí mismo al principio, el autor entra directamente en el argumento principal: Dios, que habló en el pasado a través de los profetas, ahora nos ha hablado a través de su Hijo (Heb. 1:1, 2). Muchos creyentes consideran que este es uno de los pasajes más hermosos del Nuevo Testamento, no solo por su estilo retórico, sino también por su profunda teología.",
    },
    {
      type: "verse",
      reference: "Hebreos 1:1-4",
      text: "Dios, habiendo hablado muchas veces y de muchas maneras en otro tiempo a los padres por los profetas, en estos postreros días nos ha hablado por el Hijo, a quien constituyó heredero de todo, y por quien asimismo hizo el universo; el cual, siendo el resplandor de su gloria, y la imagen misma de su sustancia, y quien sustenta todas las cosas con la palabra de su poder, habiendo efectuado la purificación de nuestros pecados por medio de sí mismo, se sentó a la diestra de la Majestad en las alturas, hecho tanto superior a los ángeles, cuanto heredó más excelente nombre que ellos.",
    },
    {
      type: "paragraph",
      text: "El autor de Hebreos afirma que Dios nos habló a través de Jesús, quien es superior a los profetas, a los ángeles, a Moisés, a Josué y a todos los demás. De hecho, Jesús es el 'resplandor de su gloria, y la imagen misma de su sustancia'. Además, Jesús 'sustenta todas las cosas con la palabra de su poder'. Estos son atributos divinos. El autor también afirma que Jesús 'efectuó la purificación de nuestros pecados' y 'se sentó a la diestra de la Majestad en las alturas'. Jesús es tanto Creador como Redentor.",
    },
    {
      type: "paragraph",
      text: "La carta a los Hebreos es un documento rico en imágenes del santuario. Compara el ministerio terrenal de Jesús con su ministerio celestial. Muestra que el cielo contiene un santuario, que es el modelo del santuario terrenal construido por Moisés. El ministerio de Jesús en el santuario celestial es superior al ministerio de los sacerdotes en el santuario terrenal, así como la nueva alianza es superior a la antigua.",
    },
  ],
};

export default function LessonDayPage({ params }: { params: { week: string; day: string } }) {
  const [activeAITool, setActiveAITool] = useState<string | null>(null);
  const [reflection, setReflection] = useState("");
  const [isCompleted, setIsCompleted] = useState(false);
  const [openVerseDialog, setOpenVerseDialog] = useState(false);
  const [selectedVerse, setSelectedVerse] = useState<{
    reference: string;
    text: string;
  } | null>(null);

  const handleAIToolClick = (tool: string) => {
    setActiveAITool(activeAITool === tool ? null : tool);
  };

  const handleVerseClick = (verse: { reference: string; text: string }) => {
    setSelectedVerse(verse);
    setOpenVerseDialog(true);
  };

  const markAsStudied = () => {
    setIsCompleted(true);
    // In a real app, this would update the Redux store or make an API call
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Banner Image */}
      <div className="relative w-full h-64">
        <Image
          src={lessonData.bannerImage || "/placeholder.svg"}
          alt={lessonData.title}
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-black/40 flex items-end">
          <div className="container p-6">
            <h1 className="text-3xl font-bold text-white mb-2">{lessonData.dayTitle}</h1>
            <p className="text-white/90">{lessonData.subtitle}</p>
          </div>
        </div>
      </div>

      {/* Lesson Content */}
      <div className="container py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {lessonData.content.map((item, index) => {
              if (item.type === "paragraph") {
                return (
                  <div key={index} className="group relative">
                    <p className="text-lg leading-relaxed">{item.text}</p>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute right-0 top-0 opacity-0 group-hover:opacity-100 transition-opacity"
                      onClick={() => handleAIToolClick(`paragraph-${index}`)}
                    >
                      <PsychologyAlt className="h-5 w-5" />
                    </Button>

                    {activeAITool === `paragraph-${index}` && (
                      <Card className="mt-4">
                        <CardContent className="p-4">
                          <Tabs defaultValue="explain">
                            <TabsList className="grid w-full grid-cols-3">
                              <TabsTrigger value="explain">Explicar</TabsTrigger>
                              <TabsTrigger value="reflect">Reflexionar</TabsTrigger>
                              <TabsTrigger value="apply">Aplicar</TabsTrigger>
                            </TabsList>
                            <TabsContent value="explain" className="p-4">
                              <p>
                                Este párrafo destaca la importancia de Jesús como el medio definitivo por el cual Dios
                                se ha comunicado con la humanidad. A diferencia de las comunicaciones anteriores a
                                través de los profetas, Jesús representa la revelación completa y perfecta de Dios.
                              </p>
                            </TabsContent>
                            <TabsContent value="reflect" className="p-4">
                              <p>
                                ¿De qué manera has experimentado la comunicación de Dios en tu vida? ¿Cómo te ayuda
                                saber que Jesús es la revelación definitiva de Dios a entender mejor el carácter divino?
                              </p>
                            </TabsContent>
                            <TabsContent value="apply" className="p-4">
                              <p>
                                Considera dedicar tiempo esta semana a estudiar más profundamente quién es Jesús según
                                Hebreos 1. Reflexiona sobre cómo su superioridad afecta tu adoración y tu confianza en
                                Él como tu Salvador.
                              </p>
                            </TabsContent>
                          </Tabs>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                );
              } else if (item.type === "verse") {
                return (
                  <Card
                    key={index}
                    className="bg-primary/5 hover:bg-primary/10 transition-colors cursor-pointer"
                    onClick={() => handleVerseClick(item as { reference: string; text: string })}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start gap-2">
                        <BookOpen className="h-5 w-5 mt-1 flex-shrink-0" />
                        <div>
                          <p className="font-medium">{item.reference}</p>
                          <p className="mt-1 text-sm">{item.text}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              }
              return null;
            })}

            {/* Reflection Section */}
            <div className="mt-8 border-t pt-6">
              <h2 className="text-xl font-bold mb-4">Mi Reflexión</h2>
              <Textarea
                placeholder="Escribe tus pensamientos, preguntas o aplicaciones personales aquí..."
                className="min-h-32 mb-4"
                value={reflection}
                onChange={(e) => setReflection(e.target.value)}
              />
              <div className="flex justify-between">
                <Button variant="outline" className="gap-2">
                  <Share2 className="h-4 w-4" />
                  Compartir con mi Grupo
                </Button>
                <Button onClick={markAsStudied} disabled={isCompleted} className="gap-2">
                  <Check className="h-4 w-4" />
                  {isCompleted ? "Completado" : "Marcar como Estudiado"}
                </Button>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card>
              <CardContent className="p-4">
                <h3 className="font-bold mb-2">Navegación de Lección</h3>
                <div className="grid grid-cols-7 gap-2">
                  {["S", "D", "L", "M", "M", "J", "V"].map((day, i) => (
                    <Button
                      key={i}
                      variant={params.day === String(i + 1) ? "default" : "outline"}
                      className="w-full h-10"
                      asChild
                    >
                      <a href={`/lesson/${params.week}/${i + 1}`}>{day}</a>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <h3 className="font-bold mb-2">Recursos Adicionales</h3>
                <ul className="space-y-2">
                  <li>
                    <a href="#" className="text-primary hover:underline">
                      Comentario Bíblico
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-primary hover:underline">
                      Guía del Maestro
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-primary hover:underline">
                      Preguntas de Discusión
                    </a>
                  </li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Bible Verse Dialog */}
      <Dialog open={openVerseDialog} onOpenChange={setOpenVerseDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{selectedVerse?.reference}</DialogTitle>
          </DialogHeader>
          <div className="mt-4">
            <p>{selectedVerse?.text}</p>
          </div>
          <div className="mt-4">
            <Tabs defaultValue="rvr1960">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="rvr1960">RVR 1960</TabsTrigger>
                <TabsTrigger value="nvi">NVI</TabsTrigger>
                <TabsTrigger value="dhh">DHH</TabsTrigger>
              </TabsList>
              <TabsContent value="rvr1960" className="p-4">
                <p>{selectedVerse?.text}</p>
              </TabsContent>
              <TabsContent value="nvi" className="p-4">
                <p>Versión en NVI del texto bíblico seleccionado.</p>
              </TabsContent>
              <TabsContent value="dhh" className="p-4">
                <p>Versión en DHH del texto bíblico seleccionado.</p>
              </TabsContent>
            </Tabs>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

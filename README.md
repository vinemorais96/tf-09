No encapsulamento, a interface pública do Atalho é a propriedade destino (somente leitura) e o método redirecionar(), enquanto o atributo __destino fica restrito em __slots__ e protegido contra referências circulares.
Na herança, a interface expõe o contrato herdado de Item (caminho, pai, mover_para), ficando oculta a reutilização interna da estrutura base sem código duplicado.
No polimorfismo, a interface padroniza a chamada de tamanho() e mostrar() compatíveis com Medivel, ocultando a regra interna de custo fixo de 1 byte e a formatação de redirecionamento.

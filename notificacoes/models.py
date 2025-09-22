from django.db import models
from django.core.mail.backends.smtp import EmailBackend
from casos.models import Workflow, FaseWorkflow

class ConfiguracaoEmail(models.Model):
    apelido = models.CharField(max_length=100, help_text="Ex: E-mail Principal do Sistema")
    email_host = models.CharField(max_length=100, verbose_name="Servidor SMTP (Ex: smtp.gmail.com)")
    email_port = models.PositiveIntegerField(default=587, verbose_name="Porta")
    email_host_user = models.EmailField(verbose_name="Usuário (e-mail de envio)")
    email_host_password = models.CharField(max_length=100, verbose_name="Senha (ou Senha de App do Google)")
    email_use_tls = models.BooleanField(default=True, verbose_name="Usar TLS")
    ativo = models.BooleanField(default=False, help_text="Apenas UMA configuração pode estar ativa para notificações automáticas.")

    def __str__(self):
        return self.apelido

    def save(self, *args, **kwargs):
        if self.ativo:
            ConfiguracaoEmail.objects.filter(ativo=True).update(ativo=False)
        super().save(*args, **kwargs)
    
    def get_connection(self):
        return EmailBackend(
            host=self.email_host, port=self.email_port, username=self.email_host_user,
            password=self.email_host_password, use_tls=self.email_use_tls
        )

    class Meta:
        verbose_name = "Configuração de Servidor de E-mail"

class TemplateEmail(models.Model):
    TIPO_CONTEUDO_CHOICES = (('texto', 'Texto Simples'), ('html', 'HTML'))
    
    apelido = models.CharField(max_length=100, unique=True, help_text="Nome interno para identificar este template. Ex: 'Notificação de Avanço de Fase'")
    assunto = models.CharField(max_length=200)
    tipo_conteudo = models.CharField(max_length=5, choices=TIPO_CONTEUDO_CHOICES, default='html')
    corpo = models.TextField(verbose_name="Corpo do E-mail", help_text="Use variáveis como {{ caso.id }}, {{ caso.titulo_caso }}, {{ cliente.nome_razao_social }}, {{ fase_origem.nome }}, {{ fase_destino.nome }}.")

    def __str__(self):
        return self.apelido

    class Meta:
        verbose_name = "Template de E-mail"
        verbose_name_plural = "Templates de E-mail"

class RegraNotificacao(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name="Para o Workflow")
    fase_de_origem = models.ForeignKey(FaseWorkflow, on_delete=models.CASCADE, related_name="regras_de_saida", verbose_name="Quando sair da Fase")
    fase_de_destino = models.ForeignKey(FaseWorkflow, on_delete=models.CASCADE, related_name="regras_de_entrada", verbose_name="E entrar na Fase")
    template_email = models.ForeignKey(TemplateEmail, on_delete=models.PROTECT, verbose_name="Usar o Template de E-mail")
    destinatarios = models.TextField(help_text="Separe múltiplos e-mails por vírgula.")

    def __str__(self):
        return f"Notificação de {self.fase_de_origem.nome} -> {self.fase_de_destino.nome}"
        
    class Meta:
        verbose_name = "Regra de Notificação"
        verbose_name_plural = "Regras de Notificação"
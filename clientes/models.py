from django.db import models

# Modelo para os Telefones
class Telefone(models.Model):
    TIPO_CHOICES = (
        ('CEL', 'Celular'),
        ('COM', 'Comercial'),
        ('RES', 'Residencial'),
    )
    
    # Relacionamento: Cada telefone pertence a UM cliente.
    # O related_name='telefones' nos permite fazer cliente.telefones.all()
    # O on_delete=models.CASCADE significa que se o cliente for apagado, seus telefones também serão.
    cliente = models.ForeignKey('Cliente', related_name='telefones', on_delete=models.CASCADE)
    
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    ddd = models.CharField(max_length=2)
    numero = models.CharField(max_length=15)

    def __str__(self):
        return f"({self.ddd}) {self.numero} - {self.get_tipo_display()}"


# Modelo Principal do Cliente
class Cliente(models.Model):
    TIPO_PESSOA_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    # --- Dados Principais ---
    tipo_pessoa = models.CharField(max_length=2, choices=TIPO_PESSOA_CHOICES, default='PF')
    nome_razao_social = models.CharField(max_length=150, help_text="Nome completo se for PF, Razão Social se for PJ")
    email = models.EmailField(max_length=100, unique=True)
    
    # --- Dados de Contato (para PJ) ---
    # blank=True e null=True significam que o campo é opcional.
    nome_contato = models.CharField(max_length=100, blank=True, null=True, help_text="Preencher apenas se for Pessoa Jurídica")
    
    # --- Endereço (campos que serão preenchidos pela API) ---
    cep = models.CharField(max_length=9) # Formato XXXXX-XXX
    logradouro = models.CharField(max_length=200, blank=True)
    numero_endereco = models.CharField(max_length=10, blank=True) # O número o usuário digita
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)
    
    # --- Metadados ---
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome_razao_social

    # Propriedade para facilitar o acesso ao nome de contato correto
    @property
    def contato_principal(self):
        if self.tipo_pessoa == 'PF':
            return self.nome_razao_social
        return self.nome_contato
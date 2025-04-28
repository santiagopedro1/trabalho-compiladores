x::Int = 0
y::Float64 = 0.0
flag::Bool = true

println("Digite um número inteiro")
x = parse(Int, readline())

println("Digite um número real")
y = parse(Float64, readline())

z = x + y

function checar(z)
    if z > 10
        println("A soma é maior que 10")
    else
        println("A soma é menor ou igual a 10")
    end
end

checar(z)

println("Resultado: ", z)
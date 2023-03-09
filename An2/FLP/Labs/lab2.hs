import Control.Applicative
import Data.Char

newtype Parser a = Parser {apply :: String -> [(a, String)]}

instance Functor Parser where
    fmap f pa = Parser (\input -> [(f a, rest) | (a, rest) <- apply pa input])

instance Applicative Parser where
    pure a = Parser (\input -> [(a, input)])
    pf <*> pa = Parser (\input -> [(f a, resta) | (f, restf) <- apply pf input, (a, resta) <- apply pa restf])

instance Monad Parser where
    pa >>= k = Parser (\input -> [(b, restb) | (a, resta) <- apply pa input, (b, restb) <- apply (k a) resta])

instance Alternative Parser where
    empty = Parser (\input -> [])
    p <|> p' = Parser (\input -> apply p input ++ apply p' input)


satisfy :: (Char -> Bool) -> Parser Char
satisfy p = Parser go
    where
        go [] = []
        go (x:xs)
            | p x = [(x, xs)]
            | otherwise = []


anychar :: Parser Char
anychar = Parser go
    where
        go [] = []
        go (x:xs) = [(x, xs)]


char :: Char -> Parser Char
char c = Parser go
    where
        go [] = []
        go (x:xs)
            | x == c = [(x, xs)]
            | otherwise = []


digit :: Parser Char
digit = Parser go
    where
        go [] = []
        go (x:xs)
            | isDigit x = [(x, xs)]
            | otherwise = []


space :: Parser Char
space = Parser go
    where
        go [] = []
        go (x:xs)
            | isSpace x = [(x, xs)]
            | otherwise = []

endOfInput :: Parser ()
endOfInput = Parser go
    where
        go "" = [((), "")]
        go _ = []


parse :: Parser a -> String -> Either String a
parse pa input =
    let res = apply (pa <* endOfInput) input
    in
        if null res then Left "Sirul de intrare nu a fost complet consumat sau parsare ambigua"
        else let [(y, rest)] = res
            in Right y


cifraSemn :: Parser Int
cifraSemn
    = do
        c <- anychar
        d <- digit
        if c == '+' then return (digitToInt d)
        else if c == '-' then return (-1 * (digitToInt d))
        else empty


string :: String -> Parser String
string [] = Parser (\input -> [("", input)])
string (x:xs) =
    do
    c <- anychar
    y <- string xs
    if c /= x then empty
    else
        return ([c] ++ y)


cifra :: Parser Int
cifra = Parser go
    where
        go [] = []
        go (x:xs)
            | isDigit x = [(digitToInt x, xs)]
            | otherwise = []


naiveNaturalHelper :: Int -> Parser Int
naiveNaturalHelper x = do
    c <- cifra
    return (x + c) <|> naiveNaturalHelper ((x + c) * 10)


naiveNatural :: Parser Int
naiveNatural = naiveNaturalHelper 0


whiteSpace :: Parser ()
whiteSpace = do
    x <- many space
    return ()


nat :: Parser Int
nat = do
    c <- some cifra
    return (foldl (\b a -> b * 10 + a) 0 c)


lexeme :: Parser a -> Parser a
lexeme pa = do
    lex <- pa
    trash <- many space
    return lex


natural :: Parser Int
natural = lexeme nat


symbol :: String -> Parser String
symbol word = lexeme (string word)


reserved :: String -> Parser ()
reserved word = do
    x <- symbol word
    return ()


comma :: Parser ()
comma = reserved ","


stopper :: Char -> Parser String
stopper s = do
    c <- anychar
    if c == s then return ""
    else do
        y <- stopper s
        return (c : y)


parens :: Parser String
parens = do
    char '('
    content <- stopper ')'
    many space
    return content


brackets :: Parser String
brackets = do
    char '['
    content <- stopper ']'
    many space
    return content


commaSep1 :: Parser a -> Parser [a]
commaSep1 pa = do
    x <- pa
    xs <- many (comma *> pa)
    return (x : xs)


commaSep :: Parser a -> Parser [a]
commaSep pa = Parser (\input -> [([], input)]) <|> (commaSep1 pa)


ident :: Parser Char -> Parser Char -> Parser String
ident identStart identLitera = do
    x <- identStart
    xs <- many identLitera
    return (x : xs)


identifier :: Parser Char -> Parser Char -> Parser String
identifier identStart identLitera = lexeme (ident identStart identLitera)